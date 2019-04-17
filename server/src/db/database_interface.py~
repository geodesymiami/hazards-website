from ..types import *

def get_info_by_hazard(hazard_type: HazardType) -> List[Hazard]:
    """
    Returns a list of Hazard
    :returns [Hazard]
    """
    pass


def get_satellites_by_hazard(hazard_id: str) -> List[Satellite]:
    """
    Returns a list of Satellite
    :returns [Satellite]
    """
    pass


def get_hazard_data_by_hazard_id(hazard_id: str, filter: HazardInfoFilter) -> Tuple[Hazard, List[Image]]:
    """
    Returns hazards by id filtered by satellite, image type, date range, and num images.
    This should constitute a multiple table lookup, where first, the data for the provided
    `hazard_id` is pulled from the `hazards` table, then the images associated with the
    `hazard_id` are pulled from the `images` table.
    :returns Hazard, [Image]
    """
    pass


"""
All database insertion methods should take care to do the following:
    1) Connect appropriately to the database
    2) Validate that the data sent to the method is valid for insertion
    3) Check to make sure that data is not added to the database multiple times
    4) Insert the data as necesarry
    5) Disconnect appropriately from the database
    6) Return a SUCCESS or FAILURE to the user
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
