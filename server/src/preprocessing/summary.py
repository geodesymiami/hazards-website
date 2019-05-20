from osgeo import gdal
import sys
import pandas as pd

import common.config.config as config
from common.types import *
from common.rsmas_logging import RsmasLogger, loglevel

ACCESS_KEY = config.get_config_var("aws_s3", "access_key")
SECRET_KEY = config.get_config_var("aws_s3", "secret_key")

def get_id_from_coords(lat, lon):

    path = os.path.abspath("resources/volcanos.csv")

    all_volcanos = pd.read_csv(path)

    lats = all_volcanos['Latitude']

    lat_sorted = all_volcanos.ix[(lats - lat).abs().argsort()]
    lat_sorted = lat_sorted[:10]
    lat_sorted = lat_sorted.reset_index(drop=True)

    lons = lat_sorted['Longitude']

    lon_sorted = lat_sorted.ix[(lons - lon).abs().argsort()]

    return all_volcanos.loc[all_volcanos['Volcano Number'] == lon_sorted.iloc[0]['Volcano Number']]


def get_bounding_box(ul_coords, x, y):

    center_lat = ul_coords[3] + ul_coords[-1] * (y / 2)
    center_lon = ul_coords[0] + ul_coords[1] * (x / 2)
    center_coords = (center_lat, center_lon)

    return center_coords


def pull_summary_data(file_path):

    logger = RsmasLogger('pipeline')

    gdal.UseExceptions()

    gdal.SetConfigOption('AWS_REGION', 'us-east-2')
    gdal.SetConfigOption('AWS_SECRET_ACCESS_KEY', SECRET_KEY)
    gdal.SetConfigOption('AWS_ACCESS_KEY_ID', ACCESS_KEY)

    try:
        ds = gdal.Open(file_path)
        ul_coords = ds.GetGeoTransform()
        x = ds.RasterXSize
        y = ds.RasterYSize
    except:
        logger.log(loglevel.ERROR, "\tThere was an error opening the file, {}, in gdal.".format(file_path))
        logger.log(loglevel.ERROR, "\t\t{}".format(gdal.GetLastErrorMsg()))
        return

    center_coords = get_bounding_box(ul_coords, x, y)

    volcano = get_id_from_coords(center_coords[0], center_coords[1])
    volcano_id = volcano["Volcano Number"].item()
    volcano_name = volcano["Volcano Name"].item()

    band = ds.GetRasterBand(1)

    satellite_name = band.GetMetadataItem('SAT')
    sat_direction = 1 if band.GetMetadataItem('Mode') == 'Asc' else 0
    image_type = band.GetMetadataItem('Image_Type')
    image_date = band.GetMetadataItem('Date')

    logger.log(loglevel.DEBUG, "\tImage Metadata:")
    logger.log(loglevel.DEBUG, "\t\tVolcano Number: {}".format(volcano_id))
    logger.log(loglevel.DEBUG, "\t\tVolcano Name: {}".format(volcano_name))
    logger.log(loglevel.DEBUG, "\t\tSatellite Name: {}".format(satellite_name))
    logger.log(loglevel.DEBUG, "\t\tSatellite Direction: {}".format(sat_direction))
    logger.log(loglevel.DEBUG, "\t\tImage Type: {}".format(image_type))
    logger.log(loglevel.DEBUG, "\t\tImage Date: {}".format(image_date))

    return volcano_id, volcano_name, satellite_name, sat_direction, image_type, image_date, center_coords


if __name__ == "__main__":
    print(pull_summary_data(sys.argv[1]))
