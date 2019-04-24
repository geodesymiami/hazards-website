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
                                        port=32000,
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

            location = Location(center)
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
        with self.database.cursor() as cursor:
            sql = "SELECT DISTINCT sat_id FROM `images` WHERE `haz_id`='{}'".format(hazard_id)
            cursor.execute(sql)  # Execute to the SQL statement
            result = cursor.fetchall()  # fetch all the results, since there may be several

        # satellites = []
        # for item in result:
        #     id = item['id']
        #     name = item['sat_name']
        #     ascending = item['ascending']
        #
        #     satellite = Satellite(id, name, ascending)
        #     satellites.append(satellite)

        return result

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

        id = int(hazard.hazard_id)
        name = hazard.name
        haz_type = hazard.hazard_type.value
        lat = hazard.location.center.lat
        lon = hazard.location.center.long
        updated = hazard.last_updated.to_integer()
        try:
            with self.database.cursor() as cursor:
                sql = "INSERT INTO `hazards` " \
                      "(`id`, `name`, `type`, `latitude`, `longitude`, `date`) " \
                      "VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(id, name, haz_type, lat, lon, updated)

                cursor.execute(sql)

            self.database.commit()
        except pymysql.err.IntegrityError as e:
            print(e)


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

        id = int(satellite.satellite_id)
        name = satellite.satellite_name
        asc = 1 if satellite.ascending else 0
        try:
            with self.database.cursor() as cursor:
                sql = "INSERT INTO `satellites` " \
                      "(`id`, `name`, `ascending`) " \
                      "VALUES ('{}', '{}', '{}')".format(id, name, asc)

                cursor.execute(sql)

            self.database.commit()
        except pymysql.err.IntegrityError as e:
            print(e)

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

        id = int(image.image_id)
        haz_id = int(image.hazard_id)
        sat_id = int(image.satellite_id)
        im_type = image.image_type.value
        im_date = image.image_date.to_integer()
        tif = image.tif_image_url.url
        raw = image.raw_image_url.url
        mod = image.modified_image_url.url

        # TODO: Need to validate that the hazard_id and satellite_id exist in the database already
        try:
            with self.database.cursor() as cursor:
                sql = "INSERT INTO `images` " \
                      "(`id`, `haz_id`, `sat_id`, `img_date`, `img_type`, `tif_image_url`, `raw_image_url`, `mod_image_url`) " \
                      "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"\
                    .format(id, haz_id, sat_id, im_date, im_type, tif, raw, mod)

                cursor.execute(sql)

            self.database.commit()
        except pymysql.err.IntegrityError as e:
            print(e)


if __name__ == "__main__":

    hazard = Hazard("200006", "Volcano2", HazardType.VOLCANOES, Location(LatLong(1.000, 1.000)), Date("19700101"))
    satellite = Satellite("00006", "S4", False)
    image = Image("6",
                  "200003",
                  "00003",
                  ImageType.GEO_BACKSCATTER,
                  Date("19700105"),
                  ImageURL("/test.jpg"),
                  ImageURL("/test.tif"),
                  ImageURL("/test.jpg")
                  )

    db = Database()
    sats = db.get_satellites_by_hazard_id("200001");
    #db.create_new_image(image)
    #db.create_new_satellite(satellite)
    #earthquakes = db.get_hazards_by_type(hazard_type=HazardType.VOLCANOES)
    #db.create_new_hazard(hazard)

    print(sats)
