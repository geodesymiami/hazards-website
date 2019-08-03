from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Tuple, Set
import os
from datetime import datetime, timedelta


class HazardType(Enum):
    VOLCANO     = 1
    EARTHQUAKE  = 2

    @classmethod
    def from_string(cls, string: str) -> "HazardType":
        """
        Example: HazardType.from_string("volcano")

        :param string: Either "volcano" or "earthquake"
        :raises ValueError when `string not in ("volcano", "earthquake")
        """
        upper_string = string.upper()
        if upper_string in HazardType.__members__:
            return HazardType[upper_string]
        else:
            raise ValueError("{} is not a valid hazard type".format(string))

    def to_string(self) -> str:
        """
        Converts a hazard type into a lowercase string.
        Examples: HazardType.to_string(HazardType.VOLCANOES) returns 'volcano'
                  HazardType.to_string(HazardType.EARTHQUAKES) returns 'earthquake'
        """
        return self.name.lower()

class ImageType(Enum):
    GEO_BACKSCATTER     = 1
    GEO_COHERENCE       = 2
    GEO_INTERFEROGRAM   = 3
    ORTHO_BACKSCATTER   = 4
    ORTHO_COHERENCE     = 5
    ORTHO_INTERFEROGRAM = 6

    @classmethod
    def from_string(cls, string: str) -> "ImageType":
        """
            Example: ImageType.from_string("geo_baskscatter")

            :param string: One of "geo_baskscatter", "geo_coherence", "geo_interferogram",
                                  "ortho_backscatter", "ortho_coherence", or "ortho_interferogram"
            :raises ValueError when `string` not in ("geo_baskscatter", "geo_coherence", "geo_interferogram",
                                                    "ortho_backscatter", "ortho_coherence", "ortho_interferogram")
        """
        upper_string = string.upper()
        if upper_string in ImageType.__members__:
            return ImageType[upper_string]
        else:
            raise ValueError("{} is not a valid image type".format(string))

    def to_string(self) -> str:
        """
            Converts an image type into a lowercase string.
            Example: ImageType.to_string(ImageType.GEO_BACKSCATTER) returns 'geo_backscatter'

            :returns : lowercase string representation of the self.name (see example)
        """
        return self.name.lower()

    def __str__(self):
        return self.to_string()

class Satellite(Enum):
    ERS_DESC    = 10
    ERS_ASC     = 11
    ENV_DESC    = 20
    ENV_ASC     = 21
    S1A_DESC    = 30
    S1A_ASC     = 31
    RS1_DESC    = 40
    RS1_ASC     = 41
    RS2_DESC    = 50
    RS2_ASC     = 51
    CSK_DESC    = 60
    CSK_ASC     = 61
    TSX_DESC    = 70
    TSX_ASC     = 71
    JERS_DESC   = 80
    JERS_ASC    = 81
    ALOS_DESC   = 90
    ALOS_ASC    = 91
    ALOS2_DESC  = 100
    ALOS2_ASC   = 101
    NISAR_DESC  = 110
    NISAR_ASC   = 111

    @classmethod
    def from_string(cls, string: str) -> "Satellite":
        """
            Example: Satellite.from_string("ERS_DESC")

            :param string: The satellite name followed by its direction (either ASC or DESC), separated by an '_'
            :raises ValueError when `string` not in satellite dictionary
        """
        upper_string = string.upper()
        if upper_string in Satellite.__members__:
            return Satellite[upper_string]
        else:
            raise ValueError("{} is not a valid satellite".format(string))

    @classmethod
    def from_int(cls, value: int) -> "Satellite":
        """
            Example: Satellite.from_int(10)

            :param value: The integer representation of the satellite, where the final digit represents the satellites
                          direction (0 for descending, 1 for ascending)
            :raises ValueError when `value` is not in satellite dictionary
        """
        if Satellite(value) in list(Satellite.__members__.values()):
            return Satellite(value)
        else:
            raise ValueError("{} is not a valid satellite".format(value))

    @classmethod
    def from_params(cls, sat_name: str, ascending: bool) -> "Satellite":
        """
            Example: Satellite.from_params("geo_backscatter", ascending=True)

            :param sat_name: The name of the satellite
            :param ascending: The direction of the satellite
            :raises: ValueError if (`sat_name`, `ascending`) not in satellite dictionary
        """
        upper_sat_name = sat_name.upper()
        sat_direction = "ASC" if ascending else "DESC"  # Python ternary operator

        sat_string = "{}_{}".format(upper_sat_name, sat_direction)

        if sat_string in Satellite.__members__:
            return Satellite[sat_string]
        else:
            raise ValueError("{} {} is not a valid set of satellite parameters".format(sat_name, sat_direction))

    def __str__(self) -> str:
        return self.name.upper()

    def __int__(self) -> int:
        return self.value

    def get_name(self) -> str:
        return self.name.upper().split("_")[0]

    def get_direction(self) -> int:
        return self.value % 10

    def is_ascending(self) -> bool:
        return self.get_direction() == 1

    def get_value(self):
        return str(self.value)

class LatLong:
    def __init__(self, lat: float, long: float):
        self.lat: float = lat
        self.long: float = long

class Date:
    """
    Class for dates of the format YYYY-MM-DD

    Example:
        >>> today = Date("2019-04-11")
        >>> print(today.date)
        20190411
        >>> print("The year is {0} in the {1}th month".format(today.date[:4], today.date[5:7]))
        The year is 2019 in the 04th month
    """

    def __init__(self, date: str):

        try:
            self.date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("The date {0} is not a valid date of the form \"YYYY-MM-DD\"".format(date))

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")

    def __int__(self):
        return int(self.date.timestamp())

    @classmethod
    def get_today(cls):
        """
            :returns Date: the Date representation of the current date
        """
        return Date(datetime.now().strftime("%Y-%m-%d"))

class DateRange:
    """
        This class is used for filtering images by a range of dates.
        If `start`  is not specified, Jan 1, 1970   is used (datetime(0)).
        If `end`    is not specified, current date  is used.
    """
    def __init__(self, start: Optional[Date] = Date("1970-01-01"), end: Optional[Date] = Date.get_today()):

        self.start_date: Optional[Date] = start
        self.end_date: Optional[Date] = end

    def __str__(self):
        return "[{start}, {end}]".format(start=self.start_date.date, end=self.end_date.date)

    def is_date_in_range(self, date: Date):
        """
            Checks if `date` is between start and end bounds of the DateRange
            :param date: the date to check
            :return bool: whether `date` is between start and end
        """
        return int(self.start_date) <= int(date) <= int(self.end_date)

class ImageURL:
    """
        Creates and validates a URL
    """
    def __init__(self, url: str):
        if self.is_valid_url(url):
            self.url: str = url
        else:
            raise ValueError("The url {0} is not a valid URL".format(url))

    @classmethod
    def is_valid_url(self, url):
        """
            Checks if the `url` is an image (file extension one of ["jpg", "png", "tif", "gif"]) and if
            the url string begins with "http".

            :param url: the `url` to validate
            :return: whether the `url` is properly formed and as expected
        """

        valid_http = ["http"]
        valid_extensions = [".jpg", ".png", ".tif", ".gif"]
        filename, file_extension = os.path.splitext(url)
        file_http = filename[:4]
        if file_http not in valid_http:
            return False
        return True

    def __str__(self):
        return self.url

class Location:
    def __init__(self, latitude, longitude):

        center = LatLong(latitude, longitude)

        valid_lats = self.validate_latitude(center)
        valid_lons = self.validate_longitude(center)
        if valid_lats and valid_lons:
            self.center = center
        else:
            raise ValueError("The latitude or longitude provided is out of bounds.")

    @classmethod
    def validate_latitude(cls, lat: LatLong):
        """
            Validates that `lat` is between -90˚ and 90˚ (valid latitudinal bounds)
            :param lat: the latitude
            :return: whether `lat` is between -90˚ and 90˚ latitude
        """
        return -90 <= float(lat.lat) <= 90

    @classmethod
    def validate_longitude(cls, lon: LatLong):
        """
           Validates that `lon` is between -180˚ and 180˚ (valid longitudinal bounds)
           :param lon: the longitude
           :return: whether `lon` is between -180˚ and 180˚ longitude
       """
        return -180 <= float(lon.long) <= 180

@dataclass
class Hazard:
    hazard_id: str
    name: str
    hazard_type: HazardType
    location: Location
    last_updated: Date
    num_images: int

@dataclass
class Image:
    image_id: str
    hazard_id: str
    satellite: Satellite
    image_type: ImageType
    image_date: Date
    raw_image_url: ImageURL
    tif_image_url: ImageURL
    modified_image_url: ImageURL

class HazardInfoFilter:
    """
        Creates a custom image filter for hazard images. Possible filter option include:
            - satellite(s)
            - image types(s)
            - date range
            - last N days of images
            - maximum number of images
        Also handles the generation of the correlated SQL where clause for the given filter options.
    """

    def __init__(self,
                 satellites:        Optional[List[Satellite]]   = None,
                 image_types:       Optional[List[ImageType]]   = None,
                 date_range:        Optional[DateRange]         = None,
                 max_num_images:    Optional[int]               = None,
                 last_n_days:       Optional[int]               = None):

        self.satellites: Optional[List[Satellite]] = satellites
        self.image_types: Optional[List[ImageType]] = image_types
        self.max_num_images: int = max_num_images

        # Combine date_range and last_n_days date range into a single date range
        # We use last_n_days as the start date if it exists
        if last_n_days:
            n_days_date_string = (datetime.today() - timedelta(days=last_n_days)).strftime("%Y-%m-%d")
            last_n_days_date = Date(n_days_date_string)
            if date_range is None:
                new_date_range = DateRange(start=last_n_days_date)
            else:
                new_date_range = DateRange(start=last_n_days_date, end=date_range.end_date)
        else:
            new_date_range = date_range

        self.date_range: Optional[DateRange] = new_date_range

    def generate_sql_filter(self, haz_id):
        """
            Generates the correlating 'WHERE' clause in SQL for passing to the database.
            :param haz_id: the haard id to filter by
            :return: the SQL representation of the filter as a WHERE clause
        """

        filter_sql = ""

        if self.satellites:

            sat_list = [sat.get_value() for sat in self.satellites]

            if len(sat_list) == 1:
                sat_sql = "`sat_id` = '{}'".format(sat_list[0])
            else:
                sat_list_string = "', '".join(sat_list)
                sat_sql = "`sat_id` in ('{}')".format(sat_list_string)

            filter_sql += " AND {}".format(sat_sql)

        if self.image_types:

            im_types_list = [str(imtype) for imtype in self.image_types]

            if len(im_types_list) == 1:
                imtype_sql = "`img_type` = '{}'".format(im_types_list[0])
            else:
                imtype_sql_string = "', '".join(im_types_list)
                imtype_sql = "`img_type` in ('{}')".format(imtype_sql_string)

            filter_sql += " AND {}".format(imtype_sql)

        if self.date_range:
            date_range_sql = "`img_date` BETWEEN '{}' AND '{}'".format(str(self.date_range.start_date),
                                                                       str(self.date_range.end_date))

            filter_sql += " AND {}".format(date_range_sql)

        # if self.max_num_images:
        #     max_num_sql = " LIMIT {}".format(self.max_num_images)
        #
        #     filter_sql += max_num_sql

        haz_id_sql = "`haz_id`={}".format(haz_id)

        print(haz_id_sql+filter_sql)

        return haz_id_sql+filter_sql
