from osgeo import gdal
import sys
import pandas as pd

import common.config.config as config
from common.types import *

ACCESS_KEY = config.get_config_var("aws_s3", "access_key")
SECRET_KEY = config.get_config_var("aws_s3", "secret_key")

def get_id_from_coords(lat, lon):
    all_volcanos = pd.read_csv("/Users/joshua/Desktop/insarlab/hazards-website/GVP_Volcano_List_Holocene.csv")

    lats = all_volcanos['Latitude']

    lat_sorted = all_volcanos.ix[(lats - lat).abs().argsort()]
    lat_sorted = lat_sorted[:10]
    lat_sorted = lat_sorted.reset_index(drop=True)

    lons = lat_sorted['Longitude']

    lon_sorted = lat_sorted.ix[(lons - lon).abs().argsort()]

    return all_volcanos.loc[all_volcanos['Volcano Number'] == lon_sorted.iloc[0]['Volcano Number']]


def get_date_from_file(file_path):
    file_name = os.path.splitext(file_path)[0]
    file_name = file_name.split("/")[-1]
    date = file_name.split("geo_")[1]
    return date


def get_bounding_box(ul_coords, x, y):
    ul_lat = ul_coords[3]
    ul_lon = ul_coords[0]
    ul_coords_n = (ul_lat, ul_lon)

    ur_lat = ul_coords[3]
    ur_lon = ul_coords[0] + ul_coords[1] * x
    ur_coords = (ur_lat, ur_lon)

    bl_lat = ul_coords[3] + ul_coords[-1] * y
    bl_lon = ul_coords[0]
    bl_coords = (bl_lat, bl_lon)

    br_lat = ul_coords[3] + ul_coords[-1] * y
    br_lon = ul_coords[0] + ul_coords[1] * x
    br_coords = (br_lat, br_lon)

    center_lat = ul_coords[3] + ul_coords[-1] * (y / 2)
    center_lon = ul_coords[0] + ul_coords[1] * (x / 2)
    center_coords = (center_lat, center_lon)

    return ul_coords_n, ur_coords, bl_coords, br_coords, center_coords


def pull_summary_data(file_path):

    gdal.SetConfigOption('AWS_REGION', 'us-east-2')
    gdal.SetConfigOption('AWS_SECRET_ACCESS_KEY', SECRET_KEY)
    gdal.SetConfigOption('AWS_ACCESS_KEY_ID', ACCESS_KEY)

    print(file_path)

    ds = gdal.Open(file_path)
    ul_coords = ds.GetGeoTransform()
    x = ds.RasterXSize
    y = ds.RasterYSize

    ul_coords, ur_coords, bl_coords, br_coords, center_coords = get_bounding_box(ul_coords, x, y)

    volcano = get_id_from_coords(center_coords[0], center_coords[1])
    volcano_id = volcano["Volcano Number"].item()
    volcano_name = volcano["Volcano Name"].item()

    band = ds.GetRasterBand(1)

    satellite_name = band.GetMetadataItem('SAT')
    sat_direction = 1 if band.GetMetadataItem('Mode') == 'Asc' else 0
    image_type = band.GetMetadataItem('Image_Type')
    image_date = band.GetMetadataItem('Date')

    return volcano_id, volcano_name, satellite_name, sat_direction, image_type, image_date, center_coords


if __name__ == "__main__":
    print(pull_summary_data(sys.argv[1]))
