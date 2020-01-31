#!/usr/bin/python3
""" State APIRest
"""

from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'])
def list_dict():
    """ list of objetc in dict form
    ---
    tags:
        - States
    parameters:
      - name: states
        in: path
        type: string
    responses:
      200:
        description: Show State
      404:
        description: State not found
    """
    lista = []
    dic = storage.all('State')
    for elem in dic:
        lista.append(dic[elem].to_dict())
    return (jsonify(lista))


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'])
def state_id(state_id):
    """ realize the specific action depending on method
    ---
    tags:
        - States
    parameters:
      - name: state_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Show State
      404:
        description: State not found
    """
    lista = []
    dic = storage.all('State')
    for elem in dic:
        var = dic[elem].to_dict()
        if var["id"] == state_id:
            if request.method == 'GET':
                return (jsonify(var))
            elif request.method == 'DELETE':
                aux = {}
                dic[elem].delete()
                storage.save()
                return (jsonify(aux))
    abort(404)


@app_views.route('/states', methods=['POST'])
def add_item():
    """ add a new item
    ---
    tags:
        - States
    consumes:
        - "application/json"
    produces:
        - "application/json"
    parameters:
      - name: state
        in: body
        required: true
        schema:
            "properties":
              "name":
                "type": "string"
    responses:
      201:
        description: Add a State
      404:
        description: State not found
      400:
        description: NOt a JSON or Missing name
    """
    if not request.json:
        return jsonify("Not a JSON"), 400
    else:
        content = request.get_json()
        if "name" not in content.keys():
            return jsonify("Missing name"), 400
        else:
            new_state = State(**content)
            new_state.save()
            return (jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_item(state_id):
    """ update item
    ---
    tags:
        - States
    parameters:
      - name: state_id
        in: path
        type: string
        required: true
      - name: state
        in: body
        required: true
        schema:
            "properties":
              "name":
                "type": "string"
    responses:
      200:
        description: Update a State
      404:
        description: State not found
      400:
        description: NOt a JSON
    """
    dic = storage.all("State")
    for key in dic:
        if dic[key].id == state_id:
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
