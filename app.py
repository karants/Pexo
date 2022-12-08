import os

import psycopg2
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import json
import requests
import math

from model.ExoplanetAPI import ExoplanetAPI
from model.DBConnection import DBWrite, DBRead

earth_gravity = 9.81
pc_to_ly = 3.26156
sun_pixels = 500
earth_pixels = 4.58

app = Flask(__name__)

DBWriteConnection = DBWrite()
DBReadConnection = DBRead()

@app.route('/')
def index():
    
    APIConnection = ExoplanetAPI()
    Exoplanets = APIConnection.GetExoplanetsList()
   

    return render_template('index.html', 
    exoplanets=Exoplanets,
    top10 = [DBReadConnection.GetTopHits()[_][0] for _ in range(len(DBReadConnection.GetTopHits()))],
    )

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/results', methods=['POST'])
def results():
   ChosenExoplanet = request.form.get('exoplanet')
   user_weight = request.form.get('weight')
   user_weighttype = request.form.get('weighttype')
   birthday = request.form.get('birthday')
   
   APIConnection = ExoplanetAPI()
   exoplanet_details = APIConnection.GetExoplanetDetails(ChosenExoplanet)


#    DBConnWrite2 = DBConnectionWrite()
   print(DBWriteConnection)
#    print(db)

   DBWriteConnection.LogHits(ChosenExoplanet)


   #weight calculation - Weight on Other Planet = Weight on Earth x Multiple of Earth’s Gravity
   user_weight_exoplanet = ((float(user_weight)) * ((float(exoplanet_details['pl_masse'])/float(math.pow(exoplanet_details['pl_rade'],2)))))
   print(user_weight_exoplanet)
   
   #distance calculation
   distance_from_earth = exoplanet_details['sy_dist'] * pc_to_ly

   #exoplanet features
   year_of_discovery = exoplanet_details['disc_year']
   method_of_discovery = exoplanet_details['discoverymethod']
   discovery_facility = exoplanet_details['disc_facility']

   print(birthday)
   print(type(birthday))

   #date of birth calculator
   exo_birth = (datetime.today() - datetime.strptime(birthday,'%Y-%m-%d')).days / exoplanet_details['pl_orbper']

   #ratio calculator
   exoplanet_pixels = (sun_pixels / ((sun_pixels * exoplanet_details['st_rad'])/(earth_pixels * exoplanet_details['pl_rade'])))


   if ChosenExoplanet:
       print('Request for hello page received with name=%s' % ChosenExoplanet)
       return render_template('results.html', 
        exoplanet = ChosenExoplanet, 
        exoplanet_details = exoplanet_details, 
        weight = round(user_weight_exoplanet),
        weighttype = user_weighttype, 
        exo_birth = round(exo_birth),
        exoplanet_pixels = str(exoplanet_pixels) + "px",
        year_of_discovery = year_of_discovery,
        method_of_discovery = method_of_discovery,
        discovery_facility = discovery_facility,
        orbital_period = round(exoplanet_details['pl_orbper']),
        distance = round(distance_from_earth))
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()