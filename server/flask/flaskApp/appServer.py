from . import app
from flask import request, url_for, jsonify, make_response, abort
import os

@app.route("/api/v2.0/")
def index():

    # Use os.getenv("key") to get environment variables
    #app_name = os.getenv("APP_NAME")
    app_name = "SCVR"

    if app_name:
        return f"Hello from {app_name} running in a Docker container behind Nginx!"

    return "Hello from Flask"

@app.route('/api/')
def index_t():
    return "</p>Server RSETFUL API</p>"

@app.route('/app/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    return "GET --------- OPERATIONS"
