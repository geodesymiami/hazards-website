from flask import Flask
from flask import request
from flask import abort, jsonify

app = Flask(__name__)

from common.types import *
from common.database import Database

@app.route('/api/<string:hazard_type_param>', methods=['GET'])
def get_hazards_summary_info(hazard_type_param: str):
    print("Get Hazards Summary")
    # HazardType.from_string() raises an exception if the string is not compatible
    try:
        print(hazard_type_param)
        hazard_type = HazardType.from_string(hazard_type_param)
        print(hazard_type)
    except ValueError:
        # send back an exception
        abort(400, "Hazard Type {0} does not exist.".format(hazard_type_param))
        return

    db = Database()

    data_from_db = db.get_hazards_by_type(hazard_type)

    db.close()

    data_to_return = parse_hazard_summary_info_from_db(data_from_db, hazard_type)

    return jsonify(data_to_return)

@app.route('/api/satellites/<int:hazard_id_param>', methods=['GET'])
def get_satellites_by_hazard_id(hazard_id_param: int):

    db = Database()

    satellites: List[Satellite] = db.get_satellites_by_hazard_id(hazard_id= hazard_id_param)

    db.close()

    if len(satellites) == 0:
        abort(404, "No satellites returned for hazard_id: {0}".format(hazard_id_param))

    data_to_return = [{'satellite_id':   sat.to_string(),
                       'satellite_name': sat.satellite_name
                      }
                      for sat in satellites]

    return jsonify(data_to_return)

@app.route('/api/<string:hazard_type_param>/<int:hazard_id_param>', methods=['GET'])
def get_hazards_page_data(hazard_type_param: str, hazard_id_param: str):
    """
    1. Validate the input data
            a. Validate the hazard type, image_types (argument), satellite_ids (argument),start_date (argument),
               end_date (argument), last_n_days (argument), and max_num_images (argument)
            b. max_num_images defaults to 5
    2. Make request to database for images based on hazard_id and filtered types
    3. Convert list of images into properly formatted JSON response

    """

    # 1. VALIDATE THE INPUT DATA
    # Validate hazard type
    try:
        HazardType.from_string(hazard_type_param)
    except ValueError:
        # send back an exception
        abort(404, "Hazard Type {0} does not exist.".format(hazard_type_param))

    # Validate image_types
    # If the image_types argument is specified, than a non-zero number of the specified arguments
    # should be valid. For example if image_types = 'valid_type,bad_type,valid_type', all is good.
    # However, if image_types = 'bad_type1,bad_type2', a 400 is thrown
    image_types: Optional[str] = request.args.get('image_types')
    validated_image_types: Set[ImageType] = set()

    if image_types is not None and image_types != "":
        parsed_image_types = image_types.split(',')
        for parsed_image_type in parsed_image_types:
            # Filter out bad values
            try:
                validated_image_types.add(ImageType.from_string(parsed_image_type))
            except ValueError:
                pass
        if len(validated_image_types) == 0:
            abort(400, "None of the following image types are supported: '{0}'".format(str(image_types)))

    # Validate satellite IDs

    satellite_ids: Optional[str] = request.args.get('satellites')
    validated_satellites: Set[Satellite] = set()

    if satellite_ids is not None and satellite_ids != "":
        parsed_satellite_ids = satellite_ids.split(",")
        for parsed_satellite_id in parsed_satellite_ids:
            try:
                new_sats = Satellite.from_string(parsed_satellite_id)
                validated_satellites.update(new_sats)
            except ValueError:
                # Bad satellite ID
                pass
            except AscendingParseException:
                # Bad ASC, DESC, BOTH parameter
                abort(400, "The following satellite id "
                           "is not of the form 'SATID_ASC', 'SATID_DESC', or 'SATID_BOTH': {0}".format(parsed_satellite_id))
        if len(validated_satellites) == 0:
            abort(400, "None of the following satellite ids are supported: '{0}'".format(str(satellite_ids)))

    # Validate start_date and end_date
    start_date = request.args.get('start_date')
    validated_start_date = None
    if start_date is not None: 
        if Date.is_valid_date(start_date):
            validated_start_date = Date(start_date)
          
    end_date = request.args.get('end_date')
    validated_end_date = None
    if end_date is not None: 
        if Date.is_valid_date(end_date):
            validated_end_date = Date(end_date)

    validated_date_range = None
    if start_date is not None:
        validated_date_range = DateRange(validated_start_date, validated_end_date)
    elif start_date is None and end_date is not None:
        abort(400, "A specified end_date without a specified start_date is not allowed.")

    # Validate integer values
    last_n_days: Optional[str] = request.args.get('last_n_days')
    validated_last_n_days = None
    if last_n_days is not None:
        if last_n_days.isdigit():
            validated_last_n_days = int(last_n_days)
        else:
            abort(400, "'last_n_days' should be an integer. {0} is not an integer.".format(last_n_days))

    max_num_images: Optional[str] = request.args.get('max_num_images')
    validated_max_num_images = None
    if max_num_images is not None:
        if max_num_images.isdigit():
            validated_max_num_images = int(max_num_images)
        else:
            abort(400, "'max_num_images' should be an integer. {0} is not an integer.".format(max_num_images))
    else:
        validated_max_num_images = 5

    # Both date_range and last_n_days cannot both be set
    if validated_date_range is not None and last_n_days is not None:
        abort(400, "Both start_date / end_date AND last_n_days cannot both be set. Please choose 1 or the other")

    # 2. MAKE REQUEST TO DATABASE

    # Create types to request from database
    hazard_filter = HazardInfoFilter(image_types=validated_image_types,
                                     satellites=validated_satellites,
                                     date_range=validated_date_range,
                                     max_num_images=validated_max_num_images,
                                     last_n_days=validated_last_n_days)

    db = Database()

    hazard, images = db.get_hazard_data_by_hazard_id(hazard_id=hazard_id_param,
                                                     filter=hazard_filter)
    db.close()

    # 3. FORMAT PYTHON TYPES INTO JSON RESPONSE

    # Handle error cases: hazard_id does not exist, no images returned
    if not hazard:
        abort(404, 'Hazard with id {0} does not exist'.format(hazard.hazard_id))
    if len(images) == 0:
        if validated_satellites:
            satellite_strs = [sat.to_string() for sat in validated_satellites]
        else:
            satellite_strs = str(None)
        if validated_image_types:
            image_type_strings = [im_type.to_string() for im_type in validated_image_types]
        else:
            image_type_strings = str(None)
        abort(404, "Request with the following filters "
                   "returned an empty response. \n"
                   "date range: {date_range}, \n"
                   "satellite_ids: {satellite_strs}, \n"
                   "image_types: {image_types}, \n"
                   "max_num_images: {max_num_images}, \n"
                   "last_n_days: {validated_last_n_days}"
                   .format(date_range=str(validated_date_range),
                           satellite_strs=str(satellite_strs),
                           image_types=image_type_strings,
                           max_num_images=validated_max_num_images,
                           validated_last_n_days=validated_last_n_days))

    parsed_image_dict = parse_hazard_images_from_db(images=images, hazard=hazard)

    filtered_image_dict = filter_hazard_images(parsed_image_dict, hazard_filter= hazard_filter)

    print("Hi")
    print(filtered_image_dict)

    return jsonify(filtered_image_dict)


@app.errorhandler(400)
def bad_request_error(error):
    response = jsonify({'code': 400, 'message': 'Bad Request. \n {0}'.format(error)})
    response.status_code = 400
    return response

@app.errorhandler(404)
def not_found_error(error):
    response = jsonify({'code': 404, 'message': 'Not Found. \n {0}'.format(error)})
    response.status_code = 404
    return response

def filter_hazard_images(parsed_dict, hazard_filter: HazardInfoFilter):
    satellites = list(parsed_dict['images_by_satellite'].keys())
    for satellite in satellites:
        if hazard_filter.satellites and satellite not in hazard_filter.satellites:
            del parsed_dict['images_by_satellite'][satellite]
        else:
            image_types = list(parsed_dict['images_by_satellite'][satellite].keys())
            for image_type in image_types:
                if hazard_filter.image_types and image_type not in hazard_filter.image_types:
                    del parsed_dict['images_by_satellite'][satellite][image_type]
                else:
                    new_image_list = []
                    # filter images by their date
                    for image in parsed_dict['images_by_satellite'][satellite][image_type]:
                        if hazard_filter.date_range and hazard_filter.date_range.date_in_range(image.image_date):
                            new_image_list.append(image)

                    new_image_list.sort(key=lambda im: int(im.image_date.date), reverse=True)
                    most_recent_images = new_image_list[:hazard_filter.max_num_images]

                    parsed_dict['images_by_satellite'][satellite][image_type] = most_recent_images

    return parsed_dict




def parse_hazard_summary_info_from_db(data: List[Hazard], hazard_type: HazardType):
    """
    Converts the data returned from the database into a JSON-compatible dictionary.
    See https://github.com/geodesymiami/hazards-website/blob/master/hazards_api.md#hazards-summary-endpoint
    for an example of what the JSON should look like

    :return: a dictionary that contains only JSON-compatible types (lists, dictionaries, floats, ints,
    None, booleans, and strings)
    """
    return_dict = dict()
    return_dict['hazards'] = []
    return_dict['type'] = HazardType.to_string(hazard_type)

    for hazard in data:
        hazard_dict = dict()
        hazard_dict['hazard_id'] = hazard.hazard_id
        hazard_dict['name'] = hazard.name
        hazard_dict['last_updated'] = hazard.last_updated.date
        hazard_dict['location'] = {
                                      'latitude':  hazard.location.center.lat,
                                      'longitude': hazard.location.center.long
                                  }
        return_dict['hazards'].append(hazard_dict)
    return return_dict


def parse_hazard_images_from_db(images: List[Image], hazard: Hazard):
    return_dict = dict()
    return_dict['hazard_id'] = hazard.hazard_id
    return_dict['hazard_name'] = hazard.name
    return_dict['last_updated'] = hazard.last_updated.date
    return_dict['location'] = {
                                'latitude':  hazard.location.center.lat,
                                'longitude': hazard.location.center.long
                              }

    return_dict['images_by_satellite'] = dict()
    # A reference to `return_dict['images_by_satellite']`
    image_dict = return_dict['images_by_satellite']

    for image in images:
        satellite = image.satellite.satellite_id.to_string()
        if satellite not in image_dict:
            image_dict[satellite] = {}

        image_type = image.image_type.to_string()
        if image_type not in image_dict[satellite]:
            image_dict[satellite][image_type] = []

        image_json = {
                        'image_id': image.image_id,
                        'image_date': image.image_date.date,
                        'raw_image_url': image.raw_image_url.url,
                        'tif_image_url': image.tif_image_url.url,
                        'modified_image_url': image.modified_image_url.url
                     }

        image_dict[satellite][image_type].append(image_json)

    return return_dict

if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)