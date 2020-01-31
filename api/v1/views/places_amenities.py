#!/usr/bin/python3
""" Place_amenities Restful API
"""

from models import storage
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, abort, request
from os import getenv

type = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def am_list(place_id):
    """ list of an objetc in dict form
    ---
    tags:
        - Place Amenities
    parameters:
      - name: place_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Show Amenities
      404:
        description: Amenity not found
    """
    lista = []
    dic = storage.all('Place')
    for elem in dic:
        if dic[elem].id == place_id:
            var = dic[elem].amenities
            for i in var:
                lista.append(i.to_dict())
            return (jsonify(lista))
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def am_delete(place_id, amenity_id):
    """ delete the object
    ---
    tags:
        - Place Amenities
    parameters:
      - name: place_id
        in: path
        type: string
        required: true
      - name: amenity_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Delete Amenities
      404:
        description: Amenity not found
    """
    p = storage.get("Place", place_id)
    a = storage.get("Amenity", amenity_id)
    if not a or not p:
        abort(404)
    for elem in p.amenities:
        if elem.id == a.id:
            if type == 'db':
                p.amenities.remove(a)
            else:
                p.amenity_ids.remove(a)
            p.save()
            return jsonify({})
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def add_am(place_id, amenity_id):
    """ create an amenity of a specific city
    ---
    tags:
        - Place Amenities
    parameters:
      - name: place_id
        in: path
        type: string
        required: true
      - name: amenity_id
        in: path
        type: string
        required: true
      - name: Place amenity
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
        description: Delete Amenities
      404:
        description: Amenity not found
    """
    lista = []
    obj = storage.get("Place", place_id)
    p = storage.get("Place", place_id)
    a = storage.get("Amenity", amenity_id)
    print(a)
    print("+++++++++++")
    print(p)
    if not a or not p:
        abort(404)
    for elem in p.amenities:
        if elem.id == a.id:
            return jsonify(a.to_dict())
    if type == 'db':
        p.amenities.append(a)
    else:
        p.amenity_id.append(a)
    p.save()
    return jsonify(a.to_dict()), 201
