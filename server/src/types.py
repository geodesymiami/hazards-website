from enum import Enum
from dataclasses import dataclass
from typing import Union, Tuple, NoneType
import os

class HazardType(Enum):
	VOLCANOES    = 1
	EARTHQUAKES  = 2
	
class ImageType(Enum):
	GEO_BACKSCATTER       = 1
	GEO_COHERENCE         = 2
	GEO_INTERFEROGRAM     = 3
	ORTHO_BACKSCATTER     = 4
	ORTHO_COHERENCE       = 5
	ORTHO_INTERFEROGRAM   = 6

class DatabaseSuccess(Enum):
	SUCCESS	= 1
	FAILURE = 2
	
@dataclass
class LatLong:
	lat: float
	long: float


class Date:
	def __init__(date: str):
		if is_date(date):
			self.date = date
		else:
			raise Exception()

	def is_date(possible_date: str):
		"""
		Checks if date is of format "YYYYMMDD"
		"""
		if len(possible_date) == 8:
			if possible_date.isdigit():
				if 1 <= int(possible_date[4:6]) <= 12:
					if 1 <= int(possible_date[6:]) <= 31:
						return True
		return False


@dataclass
class DateRange:		 
	start: Date
	stop: Union[Date, NoneType]



class URLType()
	def __init__(url: str):
		if isValid(url):
			self.url = url
		else:
			raise Exception()
		
	def isValid(url):
		valid_extensions = [".jpg", ".png", ".tiff", ".gif"]
		filename, file_extension = os.path.splitext(url)
		if filename[0] is not "/" or file_extension not in valid_extensions:
			return False
		return True

		

class Location:
	def __init__(center: LatLong, north: LatLong, south: LatLong, east: LatLong, west: LatLong):
		
		valid_lats = validate_latitudes(north, south)
		valid_lons = validate_longitude(east, west)

		if valid_lats and valid_lons:
			self.center = center
			self.bounding_box = {}
			self.bounding_box['North'] = north
			self.bounding_box['South'] = south
			self.bounding_box['East'] = east
			self.bounding_box['West'] = west
		else:
			raise Exception()

	def validate_latitudes(north, south):
		return -90 < float(north) < 90 and -90 < float(south) < 90
		
	def validate_longitudes(east, west):
		return float(east) < 180 and float(west) > -180
	
@dataclass
class Satellite:
	satellite_id: str
	satellite_name: str
	ascending: bool        

@dataclass
class HazardInfo:
	location: Location
	last_updated: Date
	hazard_id: str
	hazard_type: HazardType
	name: str

@dataclass
class Hazard:
	hazard_id: str
	name: str
	hazard_type: HazardType
	location: Location
	last_updated: Date

@dataclass
class Image:
	hazard_id: str
	satellite_id: str
	image_type: ImageType
	image_date: Date
	raw_image_url: URLType
	tif_image_url: URLType
	compressed_image_url: URLType
	modified_image_url: URLType
	
@dataclass
class HazardInfoFilter:
	satellite_ids: Tuple[List[str], NoneType]
	image_type: Tuple[List[ImageType], NoneType]
	date_range: Union[DateRange, NoneType]
	last_n_images: Union[int, NoneType]
	
	

def get_info_by_hazard(hazard_type: HazardType):
	"""
	Returns a list of HazardSummaryInfo
	[HazardSummaryInfo]
	"""
	pass

def get_satellites_by_hazard(hazard_id: str, hazard_type: HazardType):
	"""
	Returns a list of Satellite
	[Satellite]
	"""
	pass

def get_hazard_data_by_hazard_id(hazard_id: str, filter: HazardInfoFilter):
	"""
	Returns hazards by id filtered by satellite, image type, date range, and num images
	:returns HazardSummaryInfo, [Image]
	"""
	pass



"""
All datbase insertion methods should take care to do the following:
	1) Connect appropriately to the database
	2) Validate that the data sent to the method is valid for insertion
	3) Check to make sure that data is not added to the database multiple times
	4) Disconnect appropriately from the database
	5) Return a SUCCESS or FAILURE to the user
"""
	
def create_new_hazard(hazard: Hazard):
	"""
	Inserts the hazard object into the database `hazards` table. The `hazard` object's parameters
	should be one-to-one with the `hazards` table's columns.
	:returns DatabaseSuccess 
	"""
	pass
	
def create_new_satellite(satellite: Satellite):
	"""
	Inserts the satellite object into the database `satellites` table. The `satellite` object's parameters
	should be one-to-one with the `satellites` table's columns.
	:returns DatabaseSuccess 
	"""
	pass
	
def create_new_image(image: Image):
	"""
	Inserts the image object into the database `images` table. The `image` object's parameters
	should be one-to-one with the `images` table's columns. Also, needs to insert a new 
	`satellite_hazard` pair into the `satellite_hazards` table correlating the existence of the
	image's satellite with the image's hazard.
	:returns DatabaseSuccess 
	"""
	pass