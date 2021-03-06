from flask import Flask, Response
from flask_cors import CORS
from flask import request
from flask import abort, jsonify

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

CORS(app)

from common.types import *
from common.database import Database


def format_response(json):
    """
    Formats the API response with given headers and data
    :param json: json, the data to return as a JSON blob
    :return:
    """
    resp = Response(json, status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@app.route('/api/<string:hazard_type_param>', methods=['GET'])
def get_hazards(hazard_type_param: str):
    print("Get Hazards Summary")
    try:
        hazard_type = HazardType.from_string(hazard_type_param)
    except ValueError:
        # send back an exception
        abort(400, "Hazard Type {0} does not exist.".format(hazard_type_param))
        return

    db = Database()
    data_from_db = db.get_hazards_by_type(hazard_type)
    db.close()

    data_to_return = parse_hazard_summary_info_from_db(data_from_db, hazard_type)

    print(data_to_return)

    return jsonify(data_to_return)

@app.route('/api/satellites/<int:hazard_id_param>', methods=['GET'])
def get_satellites_by_hazard_id(hazard_id_param: int):

    db = Database()
    satellites: List[Satellite] = db.get_satellites_by_hazard_id(hazard_id=hazard_id_param)
    db.close()

    data_to_return = [{'satellite_id': sat.get_value(), 'satellite_name': str(sat)} for sat in satellites]

    return jsonify(data_to_return)

@app.route('/api/<string:hazard_type_param>/<int:hazard_id_param>', methods=['GET'])
def get_hazard_data(hazard_type_param: str, hazard_id_param: str):

    try:
        HazardType.from_string(hazard_type_param)
    except ValueError:
        # send back an exception
        abort(404, "Hazard Type {0} does not exist.".format(hazard_type_param))

    db = Database()
    hazard = db.get_hazard_info_by_hazard_id(hazard_id_param)
    db.close()

    if not hazard:
        abort(404, 'Hazard with id {0} does not exist'.format(hazard.hazard_id))

    data = parse_hazard_data_from_db(hazard)

    return jsonify(data)

@app.route('/api/<string:hazard_type_param>/images/<int:hazard_id_param>', methods=['GET'])
def get_hazard_images(hazard_type_param: str, hazard_id_param: str):
    """
    1. Validate the input data
            a. Validate the hazard type, image_types (argument), satellite_ids (argument),start_date (argument),
               end_date (argument), last_n_days (argument), and max_num_images (argument)
            b. max_num_images defaults to 5
    2. Make request to database for images based on hazard_id and filtered types
    3. Convert list of images into properly formatted JSON response

    """

    print(request.args)

    # 1. VALIDATE THE INPUT DATA
    # Validate hazard type
    try:
        HazardType.from_string(hazard_type_param)
    except ValueError:
        # send back an exception
        abort(404, "Hazard Type {0} does not exist.".format(hazard_type_param))

    # Validate satellite IDs
    satellite_ids: Optional[str] = request.args.get('satellites')
    validated_satellites = list()

    if satellite_ids is not None and satellite_ids != "":
        parsed_satellite_ids = satellite_ids.split(",")

        for parsed_satellite_id in parsed_satellite_ids:
            try:
                new_sat = Satellite.from_string(parsed_satellite_id)
                validated_satellites.append(new_sat)
            except ValueError:
                # Bad satellite ID
                pass

        if len(validated_satellites) == 0:
            abort(400, "None of the following satellite ids are supported: '{0}'".format(str(satellite_ids)))

    validated_satellites = list(set(validated_satellites))

    # Validate start_date and end_date
    start_date = request.args.get('start_date')
    validated_start_date = None
    if start_date is not None:

        if start_date == "":
            start_date = "1970-01-01"

        try:
            validated_start_date = Date(start_date)
        except ValueError:
            abort(400, "The following is an invalid date: {}".format(start_date))
    else:
        validated_start_date = Date("1970-01-01")
          
    end_date = request.args.get('end_date')
    validated_end_date = None
    if end_date is not None:

        if end_date == "":
            end_date = str(Date.get_today())

        try:
            validated_end_date = Date(end_date)
        except ValueError:
            abort(400, "The following is an invalid date: {}".format(end_date))
    else:
        validated_end_date = Date.get_today()

    validated_date_range = DateRange(validated_start_date, validated_end_date)

    # Validate integer values
    last_n_days: Optional[str] = request.args.get('last_n_days')

    validated_last_n_days = None
    if last_n_days is not None and last_n_days != '':
        if last_n_days.isdigit():
            validated_last_n_days = int(last_n_days)
        else:
            abort(400, "'last_n_days' should be an integer. {0} is not an integer.".format(last_n_days))

    max_num_images: Optional[str] = request.args.get('max_num_images')
    validated_max_num_images = None
    if max_num_images is not None and max_num_images != '':
        if max_num_images.isdigit():
            validated_max_num_images = int(max_num_images)
        else:
            abort(400, "'max_num_images' should be an integer. {0} is not an integer.".format(max_num_images))
    else:
        validated_max_num_images = 10

    # 2. MAKE REQUEST TO DATABASE

    # Create types to request from database
    hazard_filter = HazardImagesFilter(satellites=validated_satellites,
                                       date_range=validated_date_range,
                                       max_num_images=validated_max_num_images,
                                       last_n_days=validated_last_n_days)

    db = Database()

    images = db.get_images_by_hazard_id(hazard_id=hazard_id_param, filter=hazard_filter)
    db.close()

    # 3. FORMAT PYTHON TYPES INTO JSON RESPONSE

    # Handle error cases: hazard_id does not exist, no images returned
    parsed_image_dict = parse_hazard_images_from_db(images=images, hazard_id=hazard_id_param)

    return jsonify(parsed_image_dict)


@app.errorhandler(400)
def bad_request_error(error):
    response = jsonify({'code': 400, 'message': 'Bad Request. \n {0}'.format(error)})
    response.status_code = 400
    return format_response(response)

@app.errorhandler(404)
def not_found_error(error):
    response = jsonify({'code': 404, 'message': 'Not Found. \n {0}'.format(error)})
    response.status_code = 404
    return format_response(response)

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

        hazard_dict = {
            'hazard_id': hazard.hazard_id,
            'name': hazard.name,
            'latitude': hazard.location.center.lat,
            'longitude': hazard.location.center.long,
            'num_images': hazard.num_images,
            'last_updated': str(hazard.last_updated)
        }

        return_dict['hazards'].append(hazard_dict)
    return return_dict

def parse_hazard_data_from_db(hazard: Hazard):

    return_dict = {
        'hazard_id': hazard.hazard_id,
        'hazard_name': hazard.name,
        'last_updated': str(hazard.last_updated),
        'location': {
            'latitude': hazard.location.center.lat,
            'longitude': hazard.location.center.long
        },
        'num_images': hazard.num_images
    }


    return return_dict

def parse_hazard_images_from_db(images: List[Image], hazard_id: str):
    return_dict = dict()
    return_dict['hazard_id'] = hazard_id
    return_dict['images_by_type'] = dict()

    # A reference to `return_dict['images_by_satellite']`
    image_dict = return_dict['images_by_type']

    for image in images:
        imtype = str(image.image_type)
        if imtype not in image_dict:
            image_dict[imtype] = {}

        satellite = str(image.satellite)
        if satellite not in image_dict[imtype]:
            image_dict[imtype][satellite] = []

        image_json = {
                        'image_id': image.image_id,
                        'image_date': str(image.image_date),
                        'raw_image_url': str(image.raw_image_url),
                        'tif_image_url': str(image.tif_image_url),
                        'modified_image_url': str(image.modified_image_url)
                     }

        image_dict[imtype][satellite].append(image_json)

    return return_dict

if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)
