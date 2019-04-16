from ..types import *

def get_hazards_by_type(hazard_type: HazardType) -> List[Hazard]:
    """
    Returns a list of Hazard of a given HazardType.

    :param hazard_type: the type of hazard to return (volcano or earthquake)
    :returns [Hazard]
    """
    pass


def get_satellites_by_hazard_id(hazard_id: str) -> List[Satellite]:
    """
    Returns a list of Satellite that have images a given hazard (given by hazard_id)

    :param hazard_id: the hazard_id of the hazard to obtain a list of satellites for
    :returns [Satellite]
    """
    pass


def get_hazard_data_by_hazard_id(hazard_id: str, filter: HazardInfoFilter) -> Tuple[Hazard, List[Image]]:
    """
    Returns hazards by id filtered by satellite, image type, date range, and num images.
    This should constitute a multiple table lookup, where first, the data for the provided
    `hazard_id` is pulled from the `hazards` table, then the images associated with the
    `hazard_id` are pulled from the `images` table.

    :param hazard_id: the hazard_id to pull information and images for
    :param filter: a list of filtering options to refine the returned information
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
    Inserts a hazard object into the database `hazards` table. The `hazard` object's parameters
    should be one-to-one with the `hazards` table's columns.

    Some validations that should be done:
        - All parameters exist
        - All parameters are properly sanitized for database insertion
        - The hazard doesn't already exist in the database

    Also needs to take care to update the `last_updated` column to the new image date being stored.

    :param hazard: a fully formed hazard object to insert
    :returns DatabaseSuccess
    """
    pass


def create_new_satellite(satellite: Satellite):
    """
    Inserts a satellite object into the database `satellites` table. The `satellite` object's parameters
    should be one-to-one with the `satellites` table's columns.

    Some validations that should be done:
        - All parameters exist
        - All parameters are properly sanitized for database insertion
        - The satellite doesn't already exist in the database

    :param satellite: a fully formed Satellite object to insert
    :returns DatabaseSuccess
    """
    pass


def create_new_image(image: Image):
    """
    Inserts a image object into the database `images` table. The `image` object's parameters
    should be one-to-one with the `images` table's columns. Also, needs to insert a new
    `satellite_hazard` pair into the `satellite_hazards` table correlating the existence of the
    image's satellite with the image's hazard.

    Some validations that should be done:
        - All parameters exist
        - All parameters are properly sanitized for database insertion
        - The image doesn't already exist in the database (check by URL)
        - The hazard_id and satellite_id exist already in the database
        - The image_date is a valid date and within reasonable bounds

    When inserting a satellite_hazards pair into the join table, validate the following:
        - The satellite_id exists in the satellite table
        - The hazard_id exists in the hazards table
        - The satellite_hazard pair is unique

    :param image: a fully formed Image object to insert
    :returns DatabaseSuccess
    """
    pass
