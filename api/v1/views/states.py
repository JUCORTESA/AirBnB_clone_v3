#!/usr/bin/python3
""" State APIRest
"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states/', methods=['GET'])
def list_dict():
    """ list of objetc in dict form
    """
    lista = []
    dic = storage.all('State')
    for elem in dic:
        lista.append(dic[elem].to_dict())
    return (jsonify(lista))


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'])
def state_id(state_id):
    """ realize the specific action depending on method
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
