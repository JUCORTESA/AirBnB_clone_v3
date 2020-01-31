#!/usr/bin/python3
""" Amenities APIRest
"""

from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'])
def amenity_list():
    """ list of objetc in dict form
    ---
    tags:
        - Amenities
    parameters:
      - name: amenity
        in: path
        type: string
    responses:
      200:
        description: Show Amenity
      404:
        description: Amenity not found
    """
    lista = []
    dic = storage.all('Amenity')
    for elem in dic:
        lista.append(dic[elem].to_dict())
    return (jsonify(lista))


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE'])
def amenity_id(amenity_id):
    """ realize the specific action depending on method
    ---
    tags:
        - Amenities
    parameters:
      - name: amenity_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Show Amenity
      404:
        description: Amenity not found
    """
    lista = []
    dic = storage.all('Amenity')
    for elem in dic:
        var = dic[elem].to_dict()
        if var["id"] == amenity_id:
            if request.method == 'GET':
                return (jsonify(var))
            elif request.method == 'DELETE':
                aux = {}
                dic[elem].delete()
                storage.save()
                return (jsonify(aux))
    abort(404)


@app_views.route('/amenities', methods=['POST'])
def amenity_item():
    """ add a new item
    ---
    tags:
        - Amenities
    parameters:
      - name: amenity
        in: body
        required: true
        schema:
            id: amenity_id
            type: "object"
            "properties":
              "name":
                "type": "string"
    responses:
      201:
        description: Show Amenity
      404:
        description: Amenity not found
      400:
        description: Missing name or not a JSON
    """
    if not request.json:
        return jsonify("Not a JSON"), 400
    else:
        content = request.get_json()
        if "name" not in content.keys():
            return jsonify("Missing name"), 400
        else:
            new_amenity = Amenity(**content)
            new_amenity.save()
            return (jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """ update item
    ---
    tags:
        - Amenities
    parameters:
      - name: amenity_id
        in: path
        type: string
        required: true
      - name: amenity
        in: body
        required: true
        schema:
            id: amenity_id
            type: "object"
            "properties":
              "name":
                "type": "string"
    responses:
      200:
        description: Update Amenity
      404:
        description: Amenity not found
      400:
        description: Not a JSON
    """
    dic = storage.all("Amenity")
    for key in dic:
        if dic[key].id == amenity_id:
            if not request.json:
                return jsonify("Not a JSON"), 400
            else:
                forbidden = ["id", "update_at", "created_at"]
                content = request.get_json()
                for k in content:
                    if k not in forbidden:
                        setattr(dic[key], k, content[k])
                dic[key].save()
                return(jsonify(dic[key].to_dict()))
    abort(404)
