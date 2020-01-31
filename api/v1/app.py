#!/usr/bin/python3
"""
A python script that starts a Flask web application
"""
from flask import Flask, Blueprint, abort, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "Flasgger",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
        ('Access-Control-Allow-Credentials', "true"),
    ],
    "specs": [
        {
            "version": "1.0",
            "title": "HBNB API",
            "endpoint": 'v1_views',
            "description": 'RESTFul API for AirBnB clone',
            "route": '/v1/views',
        }
    ]
}
swagger = Swagger(app)


@app.errorhandler(404)
def page_not_found(error):
    """
    Function that shows 404
    """
    return (jsonify(error="Not found"), 404)


@app.teardown_appcontext
def teardown(exception=None):
    """
     Function closes the current session
    """
    storage.close()


if __name__ == '__main__':
    h = getenv('HBNB_API_HOST')
    p = getenv('HBNB_API_PORT')
    app.run(host=h, port=p, threaded=True)
