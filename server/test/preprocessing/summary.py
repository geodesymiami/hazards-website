from osgeo import gdal
import os
import pandas as pd

def get_id_from_coords(ul_coords, br_coords):
	ul_lat, ul_lon = ul_coords
	br_lat, br_lon = br_coords
	
	all_volcanos = pd.read_csv("/Users/joshua/Desktop/insarlab/hazards-website/GVP_Volcano_List_Holocene.csv")
	
	lats = all_volcanos['Latitude']
	lons = all_volcanos['Longitude']
	
	volcanos_in_range = all_volcanos[(lats.between(br_lat, ul_lat, inclusive=True)) & (lons.between(ul_lon, br_lon, inclusive=True))]
	
	indices = volcanos_in_range.index.tolist()
	
	volcanos = {}
	for i in indices:
		
		volcano = all_volcanos.iloc[i]
			
		volc_id = volcano['Volcano Number']
		volc_name = volcano['Volcano Name']
	
		volcanos[volc_id] = volc_name
	
	return volcanos
	

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
	ur_lon = ul_coords[0] + ul_coords[1]*x
	ur_coords = (ur_lat, ur_lon)
	
	bl_lat = ul_coords[3] + ul_coords[-1]*y
	bl_lon = ul_coords[0]
	bl_coords = (bl_lat, bl_lon)
	
	br_lat = ul_coords[3] + ul_coords[-1]*y
	br_lon = ul_coords[0] + ul_coords[1]*x
	br_coords = (br_lat, br_lon)
	
	center_lat = ul_coords[3] + ul_coords[-1]*(y/2)
	center_lon = ul_coords[0] + ul_coords[1]*(x/2)
	center_coords = (center_lat, center_lon)
	
	return ul_coords_n, ur_coords, bl_coords, br_coords, center_coords



def pull_summary_data(file_path):
	ds = gdal.Open(file_path)
	ul_coords = ds.GetGeoTransform()
	x = ds.RasterXSize
	y = ds.RasterYSize
	
	ul_coords, ur_coords, bl_coords, br_coords, center_coords = get_bounding_box(ul_coords, x, y)
	
	volcanos = get_id_from_coords(ul_coords, br_coords)
	
	if len(volcanos) is {}:
		raise Exception("No volcanos in image")
	
	#image_date = get_date_from_file(file_path)	

	satellite = ds.GetMetadataItem('satellite')
	sat_direction = ds.GetMetadataItem('sat_direction')
	image_type = ds.GetMetadataItem('type')
	image_date = ds.GetMetadataItem('date')

if __name__ == "__main__":
	os.chdir("/Users/joshua/Desktop/insarlab/hazards-website/example_data/")
	pull_summary_data('geo_20170125.tif')