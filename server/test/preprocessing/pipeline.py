import rasterio
import rasterio.plot as plot
from random import randint

from server.src.db.database import Database
import server.test.preprocessing.summary as summary
import server.test.preprocessing.image_manipulation as image
from server.src.types import *

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

    file_path = "hazards-website/Ortho_20170101_backscatter.tif"
    full_path = "/Users/joshua/Desktop/{}_full.jpg"
    mod_path = "/Users/joshua/Desktop/{}_mod.jpg"

    # 1. Read in image file
    data = rasterio.open("s3://{}".format(file_path))
    band = data.read(1)
    img = plot.show(band)

    # 2. Pull summary statistics from file
    haz_id, haz_name, sat_name, sat_dir, img_type, img_date, center = summary.pull_summary_data("/vsis3/{}".format(file_path))

    img.get_figure().savefig(full_path.format(img_date), dpi=300)

    # 3. Compress image
    compressed = image.compress_image(full_path.format(img_date), compression_amount=0.3)

    # 4 - 5. Pad image and add date on image
    text_image = image.add_text_to_image(compressed, img_date)

    # 6. Save image locally
    text_image.save(mod_path.format(img_date))

    # hazard = Hazard(haz_id, haz_name, HazardType.VOLCANO, Location(LatLong(center[0], center[1])), Date(img_date))
    # sat_id = SatelliteEnum.from_string(sat_name)
    # satellite = Satellite(sat_id, sat_dir)
    # image = Image(str(randint(1, 10000000)),
    #               haz_id,
    #               satellite,
    #               ImageType.from_string(img_type),
    #               Date(img_date),
    #               ImageURL(mod_path.format(img_date)),
    #               ImageURL(full_path.format(img_date)),
    #               ImageURL(file_path))
    #
    # db = Database()
    # db.create_new_hazard(hazard)
    # db.create_new_satellite(satellite)
    # db.create_new_image(image)
    # db.close()

