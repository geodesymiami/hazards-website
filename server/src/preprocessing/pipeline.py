import boto3
from datetime import timedelta, timezone
import logging
from random import randint
import rasterio
import rasterio.plot as plot

from common.database import Database
from common.config import config
from common.types import *
from common.rsmas_logging import RsmasLogger, loglevel

import summary as summary
import image_manipulation as immanip
import image_saveing as save


ACCESS_KEY = config.get_config_var("aws_s3", "access_key")
SECRET_KEY = config.get_config_var("aws_s3", "secret_key")
BUCKET_NAME = config.get_config_var("aws_s3", "bucket_name")

def get_list_of_images():

    s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    bucket = s3.Bucket(BUCKET_NAME)
    objects = list(bucket.objects.all())

    today = datetime.now(timezone.utc)
    delta = timedelta(days=-1)

    recent = list(
        filter(lambda o: o.last_modified.replace(tzinfo=timezone.utc).astimezone(tz=None) - today > delta, objects))
    recent = list(filter(lambda f: "tif" in os.path.splitext(f.key)[1], recent))
    recent = list(filter(lambda f: "/" not in f.key, recent))
    return recent


if __name__ == "__main__":

    """
        1. Read in image file
        2. Pull summary statistics from file
        3. Compress image
        4. Pad image as appropriate
        5. Add date onto image
        6. Save images locally
        7. Push images to S3 Bucket
        8. Remove local copies of images
        9. Create appropriate objects
        10. Push new object references to database
    """

    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.abspath("logs/{}.log".format(today))
    logger = RsmasLogger("pipeline", log_file)

    images = get_list_of_images()
    # LOG: list of images to process
    logger.log(loglevel.INFO, [img.key for img in images])

    for im in images:

        logger.log(loglevel.INFO, "Processing image: {}".format(im.key))

        file_path = "{}/{}".format(im.bucket_name, im.key)
        full_path = "{}_full.jpg"
        mod_path = "{}_mod.jpg"
        aws_path = "{}/{}/{}/{}"
        try:
            haz_id, haz_name, sat_name, sat_dir, img_type, img_date, center = summary.pull_summary_data(
                "/vsis3/{}".format(file_path))
            sat_id = Satellite.from_params(sat_name, bool(sat_dir)).value
        except:
            # LOG: error in image metadata format
            logger.log(loglevel.ERROR, '\tThere was an error in the metadata format of the image. Skipping.')
            continue

        aws_path = aws_path.format(haz_id, sat_id, img_type, img_date)
        full_path = full_path.format(img_date)
        mod_path = mod_path.format(img_date)

        # 1. Read in image file
        with rasterio.open("s3://{}".format(file_path)) as data:
            band = data.read(1)
            img = plot.show(band)
            img.get_figure().savefig(full_path, dpi=300)

        # 3. Compress image
        compressed = immanip.compress_image(full_path, compression_amount=0.3)

        # 4 - 5. Pad image and add date on image
        text_image = immanip.add_text_to_image(compressed, img_date)

        # 6. Save image locally
        text_image.save(mod_path.format(img_date))
        mod_path_aws = save.get_s3_url("{}/{}".format(aws_path, mod_path))
        full_path_aws = save.get_s3_url("{}/{}".format(aws_path, full_path))

        tif_path_aws = save.get_s3_url("{}/{}".format(aws_path, im.key))

        # LOG: images successfully moved to S3 bucket
        # LOG: mod_path_aws, full_path_aws, tif_path_aws

        hazard = Hazard(haz_id, haz_name, HazardType.VOLCANO, Location(center[0], center[1]), Date(img_date), 0)
        satellite = Satellite.from_params(sat_name, bool(sat_dir))
        image = Image(str(randint(1, 10000000)),
                      haz_id,
                      satellite,
                      ImageType.from_string(img_type),
                      Date(img_date),
                      ImageURL(full_path_aws),
                      ImageURL(tif_path_aws),
                      ImageURL(mod_path_aws))

        try:
            db = Database()
        except ConnectionError:
            logger.log(loglevel.ERROR, "\tThere was an error while connecting to the database. Skipping this image.")
            continue

        db.create_new_hazard(hazard)
        db.create_new_satellite(satellite)
        db.create_new_image(image)

        db.close()

        # LOG: database successfully updated
        logger.log(loglevel.INFO, "\tDatabase succesfully updated.")

        save.save_image_s3(mod_path, "{}/{}".format(aws_path, mod_path))
        save.save_image_s3(full_path, "{}/{}".format(aws_path, full_path))
        save.move_tif(im.key, "{}/{}".format(aws_path, im.key))

        logger.log(loglevel.INFO, "\tImages were successfully uploaded to the S3 bucket")
        logger.log(loglevel.INFO, "\t\tmod_path_aws: {}".format(mod_path_aws))
        logger.log(loglevel.INFO, "\t\tfull_path_aws: {}".format(full_path_aws))
        logger.log(loglevel.INFO, "\t\ttif_path_aws: {}".format(tif_path_aws))

        # LOG: image completed
        logger.log(loglevel.INFO, "\tProcessing of {} completed.".format(im.key))

    # LOG: finished processing images
    logger.log(loglevel.INFO, "Processing complete.")

