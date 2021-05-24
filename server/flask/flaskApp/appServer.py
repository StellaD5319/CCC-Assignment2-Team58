from . import app
from flask import request, url_for, jsonify, make_response, abort
import os
import sys 
sys.path.append("../../")
from data_analysis import city_sentiment_analysis, city_covid_analysis
db_name = "whole_au"

@app.route("/api/?city=sentiments", methods=['Get', 'POST'])
def return_sentiments_result():
    return city_sentiment_analysis._sentiment_result(db_name)

@app.route('/api/?city=covidrates', methods=['GET', 'POST'])
def return_covid_rates():
    return city_covid_analysis._covid_rate_result(db_name)

@app.route('/api/?suburb=lang', methods=['GET', 'POST'])
def return_suburb_lang_rate():
    return "GET --------- OPERATIONS"
