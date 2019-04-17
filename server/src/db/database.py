from server.src.types import *
import pymysql.cursors


class Database:

    def __init__(self):
        """
        The init constructor should handle establishing an open connection with the database,
        and handle any additional setup or connections needed for the below queries to work
        as expected. Anticipated use case of this object is as follows:

        Data Transform:
            ...
            db = Database()
            db.create_new_hazard(hazard)
            db.close()

        API:
            ...
            db = Database()
            hazards = db.get_hazards_by_type(HazardType.VOLCANOES)
            db.close()

        """

        self.HOST = ''
        self.USER = ''
        self.PASSWORD = ''
        self.DATABASE = ''

        self.database = pymysql.connect(host=self.HOST,
                                        user=self.USER,
                                        password=self.PASSWORD,
                                        db=self.DATABASE,
                                        charset='utf8mb4',
                                        cursorclass=pymysql.cursors.DictCursor)

    def close(self):
        self.database.close()

    def get_hazards_by_type(self, hazard_type: HazardType) -> List[Hazard]:
        """
        Returns a list of Hazard of a given HazardType.

        :param hazard_type: the type of hazard to return (volcano or earthquake)
        :returns [Hazard]
        """

        with self.database.cursor() as cursor:
            sql = "SELECT * FROM `hazards` WHERE `type`='{}'".format(hazard_type.value)
            cursor.execute(sql)  # Execute to the SQL statement
            result = cursor.fetchall()  # fetch all the results, since there may be several

        hazards = []
        for item in result:
            id = item['id']
            name = item['name']
            type = HazardType(item['type'])
            center = LatLong(item['latitude'], item['longitude'])

            # TODO: Change location type to ignore bounding box
            location = Location(center, center, center, center, center)
            updated = Date(str(item['last_updated']))

            hazard = Hazard(id, name, type, location, updated)
            hazards.append(hazard)

        return hazards

    def get_satellites_by_hazard_id(self, hazard_id: str) -> List[Satellite]:
        """
        Returns a list of Satellite that have images a given hazard (given by hazard_id)

        :param hazard_id: the hazard_id of the hazard to obtain a list of satellites for
        :returns [Satellite]
        """
        pass

    def get_hazard_data_by_hazard_id(self, hazard_id: str, filter: HazardInfoFilter) -> Tuple[Hazard, List[Image]]:
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

    def create_new_hazard(self, hazard: Hazard):
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

    def create_new_satellite(self, satellite: Satellite):
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

    def create_new_image(self, image: Image):
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


if __name__ == "__main__":
    db = Database()
    db.get_hazards_by_type(hazard_type=HazardType.EARTHQUAKES)
    db.close()
