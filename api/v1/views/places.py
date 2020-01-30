#!/usr/bin/python3
""" Place APIRest
"""

from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def places_list(city_id):
    """ list of objetc in dict form
    """
    lista = []
    dic = storage.all('City')
    for elem in dic:
        if dic[elem].id == city_id:
            var = dic[elem].places
            for i in var:
                lista.append(i.to_dict())
            return (jsonify(lista))
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'])
def place(place_id):
    """ list of objetc in dict form
    """
    dic = storage.all('Place')
    for elem in dic:
        if dic[elem].id == place_id:
            return (jsonify(dic[elem].to_dict()))
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def place_delete(place_id):
    """ delete the delete
    """
    dic = storage.all('Place')
    for key in dic:
        if place_id == dic[key].id:
            dic[key].delete()
            storage.save()
            return (jsonify({}))
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def add_place(city_id):
    """ create a place of a specified city
    """
    lista = []
    obj = storage.get("City", city_id)
    content = request.get_json()
    if not obj:
        abort(404)
    if not request.json:
        return (jsonify("Not a JSON"), 400)
    else:
        if "user_id" not in content.keys():
            return (jsonify("Missing user_id"), 400)
        obj2 = storage.get("User", content["user_id"])
        if not obj2:
            abort(404)
        if "name" not in content.keys():
            return (jsonify("Missing name"), 400)

        content["city_id"] = city_id
        new_place = Place(**content)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """ update specified place
    """
    dic = storage.all('Place')
    for key in dic:
        if place_id == dic[key].id:
            if not request.json:
                return (jsonify("Not a JSON"), 400)
            else:
                forbidden = ["id", "update_at", "created_at",
                             "city_id", "user_id"]
                content = request.get_json()
                for k in content:
                    if k not in forbidden:
                        setattr(dic[key], k, content[k])
                dic[key].save()
                return jsonify(dic[key].to_dict())
    abort(404)

# ----------------------advanced task ---------------------------------------


@app_views.route('/places_search', methods=['POST'])
def advanced():
    """ return all places per city, state or amenities
    return all places that has all amenities
    return all places that belong to city or state
    permited keys states, cities, amenities
    """
    content = request.get_json()
    result = []
    # rule empty body and not json file
    try:
        if (len(content) == 0 and type(content) is dict):
            dic = storage.all("Place")
            for key in dic:
                result.append(dic[key].to_dict())
            return jsonify(result)
    except:
        if not request.json:
            return (jsonify("Not a JSON"), 400)
    # rule empty permited keys
    flag = 0
    for key in content:
        if len(content[key]) > 0:
            flag = 1
    if flag == 0:
            dic = storage.all("Place")
            for key in dic:
                result.append(dic[key].to_dict())
            return jsonify(result)
    # rule 1 states
    if "states" in content.keys() and len(content["states"]) > 0:
        for i in content["states"]:
            st = storage.get("State", i)
            if st:
                for city in st.cities:
                    for place in city.places:
                        result.append(place)
    # rule 2 cities
    if "cities" in content.keys() and len(content["cities"]) > 0:
        for i in content["cities"]:
            ct = storage.get("City", i)
            if ct:
                for place in ct.places:
                    result.append(place)

    aux, result = list(set(result)), []
    for elem in aux:
        result.append(elem.to_dict())

    # rule 3 amenities
    w = "amenities"
    if w in content.keys() and len(content[w]) > 0:
        place_list = aux
        for place in place_list:
            flag = 0
            am_list = []
            am_ids = []
            amenities = place.amenities
            for am in amenities:
                am_list.append(am.to_dict())
            for elem in am_list:
                am_ids.append(elem["id"])
            for id in content[w]:
                if id not in am_ids:
                    flag = 1
                    aux.remove(place)
        aux, result = list(set(aux)), []
        for elem in aux:
            var = elem.to_dict()
            if "amenities" in var.keys():
                del var["amenities"]
            result.append(var)
    return jsonify(result)
