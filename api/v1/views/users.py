#!/usr/bin/python3
""" User APIRest
"""

from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'])
def user_list():
    """ list of objetc in dict form
    ---
    tags:
        - Users
    parameters:
      - name: user
        in: path
        type: string
        required: true
    responses:
      200:
        description: Show User
      404:
        description: User not found
    """
    lista = []
    dic = storage.all('User')
    for elem in dic:
        lista.append(dic[elem].to_dict())
    return (jsonify(lista))


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE'])
def user_id(user_id):
    """ realize the specific action depending on method
    ---
    tags:
        - Users
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Show User
      404:
        description: User not found
    """
    lista = []
    dic = storage.all('User')
    for elem in dic:
        var = dic[elem].to_dict()
        if var["id"] == user_id:
            if request.method == 'GET':
                return (jsonify(var))
            elif request.method == 'DELETE':
                aux = {}
                dic[elem].delete()
                storage.save()
                return (jsonify(aux))
    abort(404)


@app_views.route('/users', methods=['POST'])
def user_item():
    """ add a new item
    ---
    tags:
        - Users
    parameters:
      - name: city
        in: body
        required: true
        schema:
            id: city_id
            type: "object"
            "properties":
              "name":
                "type": "string"
    responses:
      201:
        description: Add User
      404:
        description: User not found
      400:
        description: Not a JSON, Missing email or Missing password
    """
    if not request.json:
        return jsonify("Not a JSON"), 400
    else:
        content = request.get_json()
        if "email" not in content.keys():
            return jsonify("Missing email"), 400
        if "password" not in content.keys():
            return jsonify("Missing password"), 400
        else:
            new_user = User(**content)
            new_user.save()
            return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """ update item
    ---
    tags:
        - Users
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
      - name: user
        in: body
        required: true
        schema:
            id: user_id
            type: "object"
            "properties":
              "name":
                "type": "string"
    responses:
      200:
        description: Update an User
      404:
        description: User not found
      400:
        description: Not a JSON
    """
    dic = storage.all("User")
    for key in dic:
        if dic[key].id == user_id:
            if not request.json:
                return jsonify("Not a JSON"), 400
            else:
                forbidden = ["id", "email", "update_at", "created_at"]
                content = request.get_json()
                for k in content:
                    if k not in forbidden:
                        setattr(dic[key], k, content[k])
                dic[key].save()
                return(jsonify(dic[key].to_dict()))
    abort(404)
