import server.src.preprocessing.image_manipulation as immanip
import server.src.common.config.config as config
import boto3
import os
from botocore.exceptions import ClientError

"""

    Should include the following functions:

    - save_image_local(image, output_path)
    - save_images_local(image, output_paths)
    - save_image_S3(image, output_path)
    - save_images_S3(image, output_paths)

"""

ACCESS_KEY = config.get_config_var("aws_s3", "access_key")
SECRET_KEY = config.get_config_var("aws_s3", "secret_key")
BUCKET = config.get_config_var("aws_s3", "bucket_name")

def save_image_local(image, output_file):
    image.save(output_file)
    return output_file


def save_image_s3(local_file, s3_file):

    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, BUCKET, s3_file)
        os.remove(local_file)
    except ClientError:
        print("Client Error")
        return

    bucket_location = s3.get_bucket_location(Bucket=BUCKET)

    object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(bucket_location['LocationConstraint'], BUCKET, s3_file)

    return object_url


def move_tif(original, new):

    s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    s3.Object(BUCKET, new).copy_from(CopySource='{}/{}'.format(BUCKET, original))
    s3.Object(BUCKET, original).delete()

    # bucket_location = s3.get_bucket_location(Bucket=BUCKET)

    object_url = "https://s3-us-east-2.amazonaws.com/{0}/{1}".format(BUCKET, new)

    return object_url


if __name__ == "__main__":
    """
    Please provide an example of how to use your functions. These test cases should
    work in general (minus the specification of the input files and output paths).
    """

    im = immanip.compress_image("/Users/joshua/Desktop/test.png")
    im = immanip.add_text_to_image(im, "Test Text 2")
    save_image_local(im, "/Users/joshua/Desktop/test2.png")
    url = save_image_s3(im, "/Users/joshua/Desktop/test2.png", "test2.png")
    print(url)

