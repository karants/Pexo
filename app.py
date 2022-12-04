import os
from dotenv import load_dotenv
import psycopg2
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import json
import requests
import math

earth_gravity = 9.81
pc_to_ly = 3.26156
sun_pixels = 500
earth_pixels = 4.58

app = Flask(__name__)

# Update connection string information
load_dotenv()
host=os.getenv('HOST')
dbname = os.getenv('DBNAME')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
sslmode = "require"
print(host)
# Construct connection string

conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)


@app.route('/')
def index():
    
   #conn = psycopg2.connect(conn_string)
   #print("Connection established")
   #cursor = conn.cursor()
   #print('Request for index page received')
   #cursor.execute('SELECT * FROM exoplanets;')
   #exoplanets = cursor.fetchall()
   #cursor.close()
   #conn.close()

   req = requests.get("https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name+from+ps+where+pl_masse+>+0+and+pl_rade+>+0+and+lower(soltype)+like+'%conf%'&format=json")
   data = json.loads(req.content)
   exoplanets=[]
   for row in data:
    for exoplanet in row.values():
        exoplanets.append(exoplanet)

   print(exoplanets)
   exoplanets_list = (list(dict.fromkeys(exoplanets)))

   return render_template('index.html', exoplanets=exoplanets_list)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/results', methods=['POST'])
def results():
   exoplanet = request.form.get('exoplanet')
   user_weight = request.form.get('weight')
   birthday = request.form.get('birthday')
   req = requests.get("https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,pl_masse,pl_rade,st_rad,sy_dist,pl_orbper,disc_year,disc_facility,discoverymethod,disc_pubdate,pl_pubdate+from+ps+where+pl_name+=+'"+exoplanet+"'+and+pl_masse+>+0+and+pl_rade+>+0+order+by+pl_pubdate+desc&format=json")
   data = json.loads(req.content)
   exoplanet_details=data[0]

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


   if exoplanet:
       print('Request for hello page received with name=%s' % exoplanet)
       return render_template('results.html', 
        exoplanet = exoplanet, 
        exoplanet_details = exoplanet_details, 
        weight = round(user_weight_exoplanet), 
        exo_birth = round(exo_birth),
        exoplanet_pixels = str(exoplanet_pixels) + "px",
        year_of_discovery = year_of_discovery,
        method_of_discovery = method_of_discovery,
        discovery_facility = discovery_facility,
        distance = round(distance_from_earth))
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()