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

@app.route('/api/<string:hazard_type>/<integer:hazard_id>', methods=['GET'])
def get_hazards_page_data(hazard_type_parameter: str, hazard_id_parameter: str):
    default_image_types = [GEO_BACKSCATTER, GEO_COHERENCE, GEO_INTERFEROGRAM, ORTHO_BACKSCATTER, ORTHO_COHERENCE, ORTHO_INTERFEROGRAM]

    image_types_requested: List = request.args.get('image_types')
    valid_types = set()
    if image_types_requested is None: 
        for type in default_image_types: # You should be able to get this info from the `ImageType` data structure
            ImageType.fromString(type)
            valid_types.add(type)
    else: 
        image_types_requested = image_types.split(',')
        for type in image_types_requested:
            if type in default_image_types:
                try:
                    ImageType.fromString(type)
                    valid_types.add(type)
                except: ValueError
                    #what do here? 
                    pass
        if len(valid_types) == 0:
            abort(400, "None of the following image types are supported: '{0}'".format(str(image_types_requested)))
    
    
    satellites_requested = request.args.get('satellites')
    satellites = set()
    if satellites_requested is not None:
        satellites_requested = satellites_requested.split(',')
        for satellite in satellites_requested:
            if satellite in SUPPORTED_SATELLITES:
                satellites.add(satellite)
        if len(satellites) == 0:
            abort(400, "None of the following satellites are supported: '{0}'".format(str(satellites_requested))
            
    start_date = request.args.get('start_date')
    if start_date is not None: 
        if Date.is_valid_date(start_date):
            pass
          
    end_date = request.args.get('end_date')
    if end_date is not None: 
        if Date.is_valid_date(end_date):
            pass
    else: 
        end_date = current_time.strftime('%m%d%y') #this right? 
        
    if start_date is not None and end_date is not None:
        pass #good stopping point
           
     
            
    
            
                  
            
    
    # If empty request, throw an exception
    
    
    # GEO_BACKSCATTER,JIBBERISH -> GEO_BACKSCATTER
    # JIBBERISH,JIBBERISH2 -> 404
    # 
    # List arguments: If None, then assume all or None whichever makes sense
    # Filter out garbage unless it's all garbage, then give them 

  
   

    # HazardType.from_string() raises an exception if the string is not compatible
    try:
        hazard_type = HazardType.from_string(hazard_type_parameter)
    except ValueError:
        # send back an exception
        abort(404, "Hazard Type {0} does not exist.".format(hazard_type_parameter))
    try:
        for type in image_list:

        image_types = HazardType.from_string(hazard_type_parameter)
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
