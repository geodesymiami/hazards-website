from flask import app
from flask import abort, jsonify
from typing import List

from ..db import database_interface
from ..types import *


@app.route('/api/<string:hazard_type>', methods=['GET'])
def get_hazards_summary_info(hazard_type_parameter: str):

    # HazardType.from_string() raises an exception if the string is not compatible
    try:
        hazard_type = HazardType.from_string(hazard_type_parameter)
    except ValueError:
        # send back an exception
        abort(404, "Hazard Type {0} does not exist.".format(hazard_type_parameter))

    data_from_db = database_interface.get_info_by_hazard(HazardType.VOLCANOES)
    data_to_return = parse_hazard_summary_info_from_db(data_from_db, hazard_type)

    return jsonify(data_to_return)


# TODO: Move parsers/converters to a separate file
def parse_hazard_summary_info_from_db(data: List[Hazard], hazard_type: HazardType):
    """
    Converts the data returned from the database into a JSON-compatible dictionary.
    See https://github.com/geodesymiami/hazards-website/blob/master/hazards_api.md#hazards-summary-endpoint
    for an example of what the JSON should look like

    :return: a dictionary that contains only JSON-compatible types (lists, dictionaries, floats, ints,
    None, booleans, and strings)
    """
    return_dict = {}
    return_dict['hazards'] = []
    return_dict['type'] = HazardType.to_string(hazard_type)

    for hazard in data:
        return_dict['hazards']['hazard_id'] = hazard.hazard_id
        return_dict['hazards']['name'] = hazard.name
        return_dict['hazards']['last_updated'] = hazard.last_updated.date
        return_dict['hazards']['location'] = {'latitude': hazard.location.center.lat,
                                              'longitude': hazard.location.center.long
                                              }
    return return_dict
