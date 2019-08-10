import time

from .types import *
from .config import config
from .rsmas_logging import RsmasLogger, loglevel

import pymysql.cursors
import sqlalchemy as sql


class Database:

    def __init__(self):
        """
        Establishes an open connection with the database.
        """
        self.pipeline_logger = RsmasLogger('pipeline')

        self.HOST = config.get_config_var("database", "localhost")
        self.USER = config.get_config_var("database", "user")
        self.PASSWORD = config.get_config_var("database", "password")
        self.DATABASE = config.get_config_var("database", "database")
        self.PORT = config.get_config_var("database", "localport")

        attempts = config.get_config_var("database", "attempts")
        delay = config.get_config_var("database", "attempt_delay")

        # Attempt to connect to the database. If the connection fails, wait and try again.
        # mysql docker service takes longer to setup than the api container, so we need to wait until
        # the mysql service is initialized before connection
        self.pipeline_logger.log(loglevel.INFO, "\tAttempting to connect to database.")
        for i in range(attempts):
            try:
                self.database = self.create_engine()
                self.conn = self.database.connect()
                self.pipeline_logger.log(loglevel.INFO, "\t\tSuccesfully connected to database after {} tries.".format(i+1))
                break
            except pymysql.err.OperationalError:
                self.pipeline_logger.log(loglevel.ERROR, "\t\tCould not connect, try #{}. Trying again.".format(i+1))
                time.sleep(delay)

        if i+1 >= attempts:
            raise ConnectionError()

    def create_engine(self):
        """
        Forms a connection to the database using the proper HOST, USER, PASSWORD, DATABASE, and PORT
        :return: pymsql.Conn, a connection object to the database
        """
        conn_string = "mysql+pymysql://{}:{}@{}:{}/{}".format(self.USER, self.PASSWORD, self.HOST, self.PORT, self.DATABASE)
        return sql.create_engine(conn_string).connect()

    def close(self):
        """
        Closes the open database connection. Should be used in conjunction with every .connect() call
        to ensure there are no open db connections of leaks.
        """
        self.database.close()

    def get_hazards_by_type(self, haz_type: HazardType) -> List[Hazard]:

        """
        Returns a list of hazards of a given HazardType.

        :param hazard_type: the type of hazard to return (volcano or earthquake)
        :returns [Hazard], the complete list of hazards of `hazard_type`
        """

        hazards = sql.Table('hazards', sql.MetaData(), autoload=True, autoload_with=self.database)
        query = sql.select([hazards]).where(hazards.columns.type == haz_type.to_string())

        result = self.conn.execute(query).fetchall()

        hazards = []
        for item in result:
            id = item['id']
            name = item['name']
            type = HazardType.from_string(item['type'])
            location = Location(item['latitude'], item['longitude'])
            last_updated = Date(item['updated'].strftime("%Y-%m-%d"))
            num_images = item['num_images']

            hazard = Hazard(id, name, type, location, last_updated, num_images)
            hazards.append(hazard)

        return hazards

    def get_satellites_by_hazard_id(self, hazard_id: int) -> List[Satellite]:
        """
        Returns a list of satellites that have images for a given hazard (given by hazard_id)
        :param hazard_id: the hazard_id of the hazard to obtain a list of satellites for
        :returns [Satellite], the list of satellites that have imaged `hazard_id`
        """

        images = sql.Table('images', sql.MetaData(), autoload=True, autoload_with=self.database)
        query = sql.select([images.columns.sat_id.distinct()]).where(images.columns.haz_id == hazard_id)

        result = self.conn.execute(query).fetchall()

        satellites = []
        for sat in result:
            sat_id = int(sat['sat_id'])
            satellites.append(Satellite.from_int(sat_id))

        return satellites
    
    def get_hazard_info_by_hazard_id(self, hazard_id: str) -> Hazard:
        """
        Returns high level information about the given `hazard_id` (whats stored in the hazards database table)
        :param hazard_id: the hazard_id of the hazard to retrieve information about
        :return: Hazard, a fully formed hazard object built from data stored in the database
        """

        hazards = sql.Table('hazards', sql.MetaData(), autoload=True, autoload_with=self.database)
        query = sql.select([hazards]).where(hazards.columns.id == hazard_id)

        result = self.conn.execute(query).fetchall()

        id = result['id']
        name = result['name']
        type = HazardType.from_string(result['type'])
        location = Location(result['latitude'], result['longitude'])
        updated = Date(result['updated'].strftime("%Y-%m-%d"))
        num_images = result['num_images']

        return Hazard(id, name, type, location, updated, num_images)

    def get_images_by_hazard_id(self, hazard_id: str, filter: Optional[HazardImagesFilter]) -> List[Image]:
        """
            Returns a list of images of the given hazard_id filtered by satellite, image type, date range,
            and number of images.

            :param hazard_id: str, the hazard_id to pull images for
            :param filter: HazardInfoFilter, a filter object containing filters by which to refine the query
            :returns [Image], a list of images matching the given filter

        """

        filter_params = filter.get_filter_params()

        images = sql.Table('images', sql.MetaData(), autoload=True, autoload_with=self.database)
        query = sql.select([images])\
                .where(images.columns.haz_id == hazard_id)\
                .where(images.columns.sat_id.in_(filter_params['satellites']))\
                .where(sql.between(images.columns.img_date, filter_params['date_start'], filter_params['date_end']))

        result = self.conn.execute(query).fetchall()

        images = []
        for item in result:

            id = item['id']
            haz_id = item['haz_id']
            sat = Satellite.from_int(int(item['sat_id']))
            img_type = ImageType.from_string(item['img_type'])
            img_date = Date(item['img_date'].strftime("%Y-%m-%d"))
            raw_img = ImageURL(item['raw_image_url'])
            mod_img = ImageURL(item['mod_image_url'])
            tif_img = ImageURL(item['tif_image_url'])

            image = Image(id, haz_id, sat, img_type, img_date, raw_img, tif_img, mod_img)
            images.append(image)

        return images

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

        :param hazard: a fully formed hazard object to insert
        """

        id = hazard.hazard_id
        name = hazard.name
        haz_type = hazard.hazard_type.value
        lat = hazard.location.center.lat
        lon = hazard.location.center.long
        updated = hazard.last_updated.date

        try:
            with self.database.cursor() as cursor:
                # TODO: sql inject secure this query
                sql = "INSERT INTO `hazards` " \
                      "(`id`, `name`, `type`, `latitude`, `longitude`, `updated`) " \
                      "VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(id, name, haz_type, lat, lon, updated)

                cursor.execute(sql)

            self.database.commit()
        except pymysql.err.IntegrityError as e:
            self.pipeline_logger.log(loglevel.WARNING, "\tThe following error occurred while inserting the new hazard into the database: {}".format(e))

    def create_new_satellite(self, satellite: Satellite):
        """
        Inserts a satellite object into the database `satellites` table. The `satellite` object's parameters
        should be one-to-one with the `satellites` table's columns.

        :param satellite: a fully formed Satellite object to insert
        """

        id = satellite.get_value()
        name = satellite.get_name()
        asc = satellite.get_direction()

        try:
            with self.database.cursor() as cursor:
                # TODO: sql inject secure this query
                sql = "INSERT INTO `satellites` " \
                      "(`id`, `name`, `direction`) " \
                      "VALUES ('{}', '{}', '{}')".format(id, name, asc)

                cursor.execute(sql)

            self.database.commit()
        except pymysql.err.IntegrityError as e:
            self.pipeline_logger.log(loglevel.WARNING, "\tThe following error occurred while inserting the new satellite into the database: {}".format(e))

    def create_new_image(self, image: Image):
        """
            Inserts a image object into the database `images` table. The `image` object's parameters
            should be one-to-one with the `images` table's columns.

            :param image: a fully formed Image object to insert
        """

        id = image.image_id
        haz_id = image.hazard_id
        sat_id = image.satellite.get_value()
        im_type = image.image_type.value
        im_date = image.image_date.date
        tif = image.tif_image_url.url
        raw = image.raw_image_url.url
        mod = image.modified_image_url.url

        try:
            with self.database.cursor() as cursor:
                # TODO: sql inject secure this query
                sql = "INSERT INTO `images` " \
                      "(`id`, `haz_id`, `sat_id`, `img_date`, `img_type`, `tif_image_url`, `raw_image_url`, `mod_image_url`) " \
                      "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')" \
                    .format(id, haz_id, sat_id, im_date, im_type, tif, raw, mod)

                cursor.execute(sql)

            self.database.commit()
        except pymysql.err.IntegrityError as e:
            self.pipeline_logger.log(loglevel.WARNING, "\tThe following error occurred while inserting the new image into the database: {}".format(e))


if __name__ == "__main__":
    hazard = Hazard("200022", "Volcano2", HazardType.VOLCANO, Location(LatLong(1.000, 1.000)), Date("19700101"), 0)
    satellite = Satellite(Satellite(9), False)
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

    # print(sats)