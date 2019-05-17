import time

from .types import *
from .config import config
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

        self.HOST = config.get_config_var("database", "localhost")
        self.USER = config.get_config_var("database", "user")
        self.PASSWORD = config.get_config_var("database", "password")
        self.DATABASE = config.get_config_var("database", "database")
        self.PORT = config.get_config_var("database", "localport")

        max_attempts = config.get_config_var("database", "attempts")
        delay = config.get_config_var("database", "attempt_delay")

        for i in range(max_attempts):
            print('Trying to connect to database')
            try:
                self.database = pymysql.connect(host=self.HOST,
                                                user=self.USER,
                                                password=self.PASSWORD,
                                                db=self.DATABASE,
                                                port=self.PORT,
                                                charset='utf8mb4',
                                                cursorclass=pymysql.cursors.DictCursor)
                break
            except:
                print("Failed {} times".format(i+1))

            time.sleep(delay)

    def close(self):
        self.database.close()

    def get_hazards_by_type(self, haz_type: HazardType) -> List[Hazard]:

        """
        Returns a list of Hazard of a given HazardType.

        :param hazard_type: the type of hazard to return (volcano or earthquake)
        :returns [Hazard]
        """

        with self.database.cursor() as cursor:
            sql = "SELECT * FROM `hazards` WHERE `type`='{}'".format(haz_type.to_string())
            cursor.execute(sql)  # Execute to the SQL statement
            result = cursor.fetchall()  # fetch all the results, since there may be several

        hazards = []
        for item in result:
            id = item['id']
            name = item['name']
            type = HazardType.from_string(item['type'])
            location = Location(LatLong(item['latitude'], item['longitude']))
            last_updated = Date(str(item['updated']))

            hazard = Hazard(id, name, type, location, last_updated)
            hazards.append(hazard)

        return hazards

    def get_satellites_by_hazard_id(self, hazard_id: str) -> List[Satellite]:
        """
        Returns a list of Satellite that have images a given hazard (given by hazard_id)
        :param hazard_id: the hazard_id of the hazard to obtain a list of satellites for
        :returns [Satellite]
        """

        with self.database.cursor() as cursor:
            sql = "SELECT satellite.* FROM satellites satellite WHERE satellite.id in " \
                  "(SELECT DISTINCT sat_id FROM images WHERE haz_id='{}')".format(hazard_id)
            cursor.execute(sql)
            result = cursor.fetchall()

        satellites = []
        for sat in result:
            id = sat['id']//10
            asc = sat['ascending'] % 10
            satellite = Satellite(id, True if asc is 1 else False)
            satellites.append(satellite)

        return satellites

    def get_hazard_data_by_hazard_id(self, hazard_id: str, filter: HazardInfoFilter) -> Tuple[Hazard, List[Image]]:
        """
        Returns hazards by id filtered by satellite, image type, date range, and num images.
        This should constitute a multiple table lookup, where first, the data for the provided
        `hazard_id` is pulled from the `hazards` table, then the images associated with the
        `hazard_id` are pulled from the `images` table.

        :param hazard_id: the hazard_id to pull information and images for
        :param filter: a list of filtering options to refine the returned information
        :returns Hazard, [Image]

        Worked on by Samuel Triana and Xinxin Rong.
        """

        images = []

        # Get Hazard data and create Hazard Object
        with self.database.cursor() as cursor:
            sql = "SELECT * FROM `hazards` WHERE `id`='{}'".format(hazard_id)
            cursor.execute(sql)  # Execute to the SQL statement
            data = cursor.fetchall()

        print(data)
        data = data[0]
        id = data['id']
        name = data['name']
        type = HazardType.from_string(data['type'])
        center = LatLong(data['latitude'], data['longitude'])

        location = Location(center)

        updated = Date(str(data['updated']).replace("-", ""))

        hazard = Hazard(id, name, type, location, updated)

        # Get Images, no filter, needs true column names
        with self.database.cursor() as cursor:
            sql = "SELECT * FROM `images` WHERE `haz_id` = '{}';".format(hazard_id)
            cursor.execute(sql)
            data = cursor.fetchall()

            for img in data:
                sat_id = int(img['sat_id']) // 10
                sat_asc = int(img['sat_id']) % 10
                print(sat_id)
                print(sat_asc)
                sat = Satellite(SatelliteEnum(sat_id), True if sat_asc == 1 else False)
                image = Image(img['id'],
                              img['haz_id'],
                              sat,
                              ImageType.from_string(img['img_type']),
                              Date(img['img_date'].strftime("%Y%m%d")),
                              ImageURL(img['raw_image_url']),
                              ImageURL(img['tif_image_url']),
                              ImageURL(img['mod_image_url'])
                              )
                images.append(image)

        return (hazard, images)

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

        print(hazard)

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

        id = satellite.satellite_id.value
        name = satellite.satellite_id.to_string()
        asc = 1 if satellite.ascending else 0

        new_id = int(str(id)+str(asc))

        try:
            with self.database.cursor() as cursor:
                sql = "INSERT INTO `satellites` " \
                      "(`id`, `name`, `ascending`) " \
                      "VALUES ('{}', '{}', '{}')".format(new_id, name, asc)

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
        sat_id = int(str(image.satellite.satellite_id.value)+str(int(image.satellite.ascending)))
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
                      "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')" \
                    .format(id, haz_id, sat_id, im_date, im_type, tif, raw, mod)

                cursor.execute(sql)

            self.database.commit()
        except pymysql.err.IntegrityError as e:
            print(e)


if __name__ == "__main__":
    hazard = Hazard("200022", "Volcano2", HazardType.VOLCANO, Location(LatLong(1.000, 1.000)), Date("19700101"))
    satellite = Satellite(SatelliteEnum(9), False)
    image = Image("60",
                  "200022",
                  satellite,
                  ImageType.GEO_BACKSCATTER,
                  Date("19700105"),
                  ImageURL("/test.jpg"),
                  ImageURL("/test.tif"),
                  ImageURL("/test.jpg")
                  )

    db = Database()

    volcanos = db.get_hazards_by_type(HazardType.VOLCANO)
    print(volcanos)
    sats = db.get_satellites_by_hazard_id("200006")
    print(sats)
    imgs = db.get_hazard_data_by_hazard_id("200006", None)
    print(imgs)

    db.create_new_hazard(hazard)
    db.create_new_satellite(satellite)
    db.create_new_image(image)

    db.close()

    # print(sats)