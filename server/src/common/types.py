from enum import Enum
from dataclasses import dataclass
from typing import Tuple, List, Optional, Set
import os
from datetime import datetime


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
            :raises ValueError when `string not in ("geo_baskscatter", "geo_coherence", "geo_interferogram",
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

    def is_ascending(self) -> bool:
        return self.value % 10 == 1

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
            self.date = datetime.strptime(date, "%y-%m-%d")
        except ValueError:
            raise ValueError("The date {0} is not a valid date of the form \"YYYY-MM-DD\"".format(date))

    def __str__(self):
        return self.date

    def __int__(self):
        return int(self.date)

    @classmethod
    def get_today(cls):
        return Date(datetime.now().strftime("%Y%m%d"))

class DateRange:
    """
    This class is used for filtering images by a range of dates.
    If `end = None`, then the date range ends on the current date
    """
    def __init__(self, start: Date, end: Optional[Date] = None):
        self.start: Date = start
        self.end: Optional[Date] = end

    def __str__(self):
        end_str = self.end.date if self.end else str(None)
        return "[{start}, {end}]".format(start=self.start.date, end=end_str)

    def date_in_range(self, date: Date):
        end_date = self.end if self.end != None else Date.get_today()
        return int(self.start) <= int(date.date) <= int(end_date)

class ImageURL():
    """
    Creates and validates a URL
    """
    def __init__(self, url: str):
        if self.is_valid_url(url):
            self.url: str = url
        else:
            raise ValueError("The url {0} is not a valid URL".format(url))

    # TODO: Add further validation
    @classmethod
    def is_valid_url(self, url):
        valid_extensions = [".jpg", ".png", ".tif", ".gif"]
        filename, file_extension = os.path.splitext(url)
        if file_extension not in valid_extensions:
            return False
        return True

class Location:
    def __init__(self, center: LatLong):

        valid_lats = self.validate_latitude(center)
        valid_lons = self.validate_longitude(center)
        if valid_lats and valid_lons:
            self.center = center
        else:
            raise Exception()

    @classmethod
    def validate_latitude(cls, lat: LatLong):
        return -90 <= float(lat.lat) <= 90

    @classmethod
    def validate_longitude(cls, lon: LatLong):
        return -180 <= float(lon.long) <= 180

class AscendingParseException(Exception):
    pass

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
    self.satellites: Optional[List[Satellite]]
    self.image_types: Optional[List[ImageType]]
    self.date_range: Optional[DateRange]
    self.max_num_images: int
    """

    def __init__(self,
                 satellites: Optional[List[Satellite]],
                 image_types: Optional[List[ImageType]],
                 date_range: Optional[DateRange],
                 max_num_images: int,
                 last_n_days: Optional[int]):

        self.satellites: Optional[List[Satellite]] = satellites
        self.image_types: Optional[List[ImageType]] = image_types
        self.max_num_images: int = max_num_images

        # Combine date_range and last_n_days date range into a single date range
        # We use last_n_days as the start date if it exists
        if last_n_days:
            last_n_days_date = Date(str(int(Date.get_today().date) - last_n_days))
            if date_range is None:
                new_date_range = DateRange(start=last_n_days_date)
            else:
                new_date_range = DateRange(start=last_n_days_date, end=date_range.end)
        else:
            new_date_range = date_range
        self.date_range: Optional[DateRange] = new_date_range
