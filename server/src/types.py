from enum import Enum
from dataclasses import dataclass
from typing import Tuple, List, Optional
import os


class HazardType(Enum):
    VOLCANOES    = 1
    EARTHQUAKES  = 2

    @classmethod
    def from_string(cls, string: str) -> "HazardType":
        """
        Example: HazardType.from_string("volcanoes")

        :param string: Either "volcanoes" or "earthquakes"
        :raises ValueError when `string not in ("volcanoes", "earthquakes")
        """
        upper_string = string.upper()
        if upper_string in HazardType.__members__:
            return HazardType[upper_string]
        else:
            raise ValueError("{} is not a valid hazard type".format(string))

    def to_string(self) -> str:
        """
        Converts a hazard type into a lowercase string.
        Examples: HazardType.to_string(HazardType.VOLCANOES) returns 'volcanoes'
                  HazardType.to_string(HazardType.EARTHQUAKES) returns 'earthquakes'
        """
        return self.name.lower()


class ImageType(Enum):
    GEO_BACKSCATTER       = 1
    GEO_COHERENCE         = 2
    GEO_INTERFEROGRAM     = 3
    ORTHO_BACKSCATTER     = 4
    ORTHO_COHERENCE       = 5
    ORTHO_INTERFEROGRAM   = 6


    @classmethod
    def from_string(cls, string: str) -> "ImageType":
        upper_string = string.upper()
        if upper_string in ImageType.__members__:
            return ImageType[upper_string]
        else:
            raise ValueError("{} is not a valid image type".format(string))


    def to_string(self) -> str:
        return self.name.lower()


class DatabaseSuccess(Enum):
    SUCCESS = 1
    FAILURE = 2


class SatelliteEnum(Enum):
    ERS   = 1
    ENV   = 2
    S1    = 3
    RS1   = 4
    RS2   = 5
    CSK   = 6
    TSX   = 7
    JERS  = 8
    ALOS  = 9
    ALOS2 = 10
    NISAR = 11

    @classmethod
    def from_string(cls, string: str) -> "SatelliteEnum":
        upper_string = string.upper()
        if upper_string in SatelliteEnum.__members__:
            return SatelliteEnum[upper_string]
        else:
            raise ValueError("{} is not a valid image type".format(string))

    def to_string(self) -> str:
        return self.name.lower()

@dataclass
class LatLong:
    lat: float
    long: float


class Date:
    """
    Class for dates of the format YYYYMMDD

    Example:
        >>> today = Date("20190411")
        >>> print(today.date)
        20190411
        >>> print("The year is {0} in the {1}th month".format(today.date[:4], today.date[4:6]))
        The year is 2019 in the 04th month
    """

    def __init__(self, date: str):
        if self.is_valid_date(date):
            self.date = date
        else:
            raise ValueError("The date {0} is not a valid date of the form \"YYYYMMDD\"".format(date))
    
    @classmethod
    def is_valid_date(self, possible_date: str):
        """
        Checks if date is of format "YYYYMMDD"
        """
        if len(possible_date) == 8:
            if possible_date.isdigit():
                if 1 <= int(possible_date[4:6]) <= 12:
                    if 1 <= int(possible_date[6:]) <= 31:
                        return True
        return False

    def to_integer(self):
        return int(self.date)


@dataclass
class DateRange:
    """
    This class is used for filtering images by a range of dates.
    If `end = None`, then the date range ends on the current date
    """
    start: Date
    end: Optional[Date]

    def __str__(self):
        end_str = self.end.date if self.end else str(None)
        return "[{start}, {end}]".format(self.start.date, end_str)

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
        if filename[0] is not "/" or file_extension not in valid_extensions:
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


@dataclass
class Satellite:
    satellite_id: SatelliteEnum
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
    image_id: str
    hazard_id: str
    satellite_id: SatelliteEnum
    image_type: ImageType
    image_date: Date
    raw_image_url: ImageURL
    tif_image_url: ImageURL
    modified_image_url: ImageURL
    
    
@dataclass
class HazardInfoFilter:
    satellite_ids: Optional[List[str]]
    image_types: Optional[List[ImageType]]
    date_range: Optional[DateRange]
    max_num_images: int
    last_n_days: int
