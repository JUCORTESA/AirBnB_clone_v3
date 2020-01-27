#!/usr/bin/python3
"""Creationg route for Blueprint
"""
from api.v1.views import app_views
import json


@app_views.route('/status')
def response():
    dic = {"status": "OK"}
    return json.dumps(dic)
