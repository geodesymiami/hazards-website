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
        Creates a HazardType object from the given `string`
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
            Creates an ImageType object from the given `string`
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
            Creates a Satellite from the given `string`
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
            Creates a Satellite from the given `value`
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
            Creates a Satellite from the given `sat_name` and direction value
            Example: Satellite.from_params("geo_backscatter", ascending=True)

            :param sat_name: The name of the satellite
            :param ascending: The direction of the satellite (True for ascending, False for descending)
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
        """
        :return: str, the name of the satellite
        """
        return self.name.upper().split("_")[0]

    def get_direction(self) -> int:
        """
        :return: str, the direction of the satellite (1 for ascending, 0 for descending)
        """
        return self.value % 10

    def is_ascending(self) -> bool:
        """
        :return: bool, True if satelliet direction is ascending, False otherwise
        """
        return self.get_direction() == 1

    def get_value(self) -> str:
        """
        :return: str, the integer representation of the satellite as a string
        """
        return str(self.value)

class LatLong:
    """
    A latitude, longitude geographic coordinate object.
    Latitude and longitude values represented as degrees N/S/E/W of the equator/prime meridian.
    """
    def __init__(self, lat: float, long: float):
        """
        :param lat: float, degrees N of the equator (negative values indicate latitude S of the equator)
        :param long: float, degrees E of the prime meridian (negative values indicate longitude W of the prime meridian)
        """
        self.lat: float = lat
        self.long: float = long

class Date:
    """
    A date of the format YYYY-MM-DD
    """

    def __init__(self, date: str):
        """
        :param date: str, the string representation of the date in YYYY-MM-DD format
        """
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
            :return Date: the Date representation of the current date
        """
        return Date(datetime.now().strftime("%Y-%m-%d"))

class DateRange:
    """
        A range of dates for filtering images by a range of dates.
    """
    def __init__(self, start: Optional[Date] = Date("1970-01-01"), end: Optional[Date] = Date.get_today()):
        """
        :param start:   Date,   the beginning date of the range,    default: 1970-01-01
        :param end:     Date,   the ending date of the range        default: current date
        """
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
    """
    A latitude, longitude location coordinate.
    Latitude and longitude are both represented as degress N/S/E/W of equator/prime meridian
    """
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

class HazardImagesFilter:
    """
        Creates a custom image filter for hazard images. Possible filter option include:
            - satellite(s)
            - date range
            - last N days of images
            - maximum number of images
        Also handles the generation of the correlated SQL where clause for the given filter options.
    """

    def __init__(self,
                 satellites:        Optional[List[Satellite]]   = None,
                 date_range:        Optional[DateRange]         = None,
                 max_num_images:    Optional[int]               = None,
                 last_n_days:       Optional[int]               = None):

        self.satellites: Optional[List[Satellite]] = satellites
        self.max_num_images: int = max_num_images

        # Combine date_range and last_n_days date range into a single date range
        # We use last_n_days as the start date if it exists
        if last_n_days:

            if date_range is None:
                n_days_date_string = (datetime.today() - timedelta(days=last_n_days)).strftime("%Y-%m-%d")
                last_n_days_date = Date(n_days_date_string)
                new_date_range = DateRange(start=last_n_days_date)
            else:
                n_days_date_string = (date_range.end_date.date - timedelta(days=last_n_days)).strftime("%Y-%m-%d")
                last_n_days_date = Date(n_days_date_string)
                new_date_range = DateRange(start=last_n_days_date, end=date_range.end_date)
        else:
            new_date_range = date_range

        self.date_range: Optional[DateRange] = new_date_range

    def get_filter_params(self):
        """
            Generates the correlating 'WHERE' clause in SQL for passing to the database.
            :param haz_id: the haard id to filter by
            :return: the SQL representation of the filter as a WHERE clause
        """

        filter_params = {
            "satellites": [],
            "date_start": '1970-01-01',
            "date_end": str(Date.get_today())
        }

        if self.satellites:

            sat_list = [sat.get_value() for sat in self.satellites]

            filter_params['satellites'] = sat_list

        if self.date_range:
            filter_params['date_start'] = self.date_range.start_date
            filter_params['date_end'] = self.date_range.end_date

        # if self.max_num_images:
        #     max_num_sql = " LIMIT {}".format(self.max_num_images)
        #
        #     filter_sql += max_num_sql

        return filter_params
