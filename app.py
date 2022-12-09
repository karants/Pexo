#This is the controller. It runs the Flask app and passes inputs and outputs between the Model and the View.

#Author: Karan Shah
#Contact: shahk47@mcmaster.ca

#Importing Pip libraries
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

#Importing classes from model directory
from model.ExoplanetAPI import ExoplanetAPI
from model.DBConnection import DBWrite, DBRead
from model.UserDetails import User
from model.PlanetarySystem import Exoplanet, Earth
from model.DesignElements import SunElement,EarthElement,ExoplanetElement,StellarElement

#Initializing Flask instance
app = Flask(__name__)

#Instantiating Database Write & Read Connections
DBWriteConnection = DBWrite()
DBReadConnection = DBRead()

#Home Route
@app.route('/')
def index():
    
    #Instantiating the ExoplanetAPI facade implementation
    APIConnection = ExoplanetAPI()

    #Returning list of exoplanets and top 10 most viewed exoplanets to the Index view
    return render_template('index.html', 
    exoplanets = APIConnection.GetExoplanetsList(),
    top10 = DBReadConnection.GetTopHits(),
    )

#Favorite Icon route
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

#Results Route
@app.route('/results', methods=['POST'])
def results():

   #Receiving the chosen exoplanet input from the user
   ChosenExoplanet = request.form.get('exoplanet')

   #Instantiating the ExoplanetAPI facade implementation and obtaining details of the chosen exoplanet
   APIConnection = ExoplanetAPI()
   PlanetaryDetails = APIConnection.GetExoplanetDetails(ChosenExoplanet)

   #Logging the Chosen Exoplanet in the hits table to track number of hits and identify the top viewed exoplanets
   DBWriteConnection.LogHits(ChosenExoplanet)

   #Instantiating the user object with input received from the end user
   user = User(request.form.get('weight'), request.form.get('weighttype'), request.form.get('birthday'))

   #Instantiating the Exoplanet and Earth Planetary System Objects with details obtained from the APIImplementation facade
   exoplanet = Exoplanet(PlanetaryDetails)
   earth = Earth()

   #Creating specific design elements for the view
   SunElementDesign = SunElement()
   EarthElementDesign = EarthElement(earth.CONST_RADIUS, earth.CONST_STELLARRADIUS, SunElementDesign.GetPixels())
   StellarElementDesign = StellarElement()  
   ExoplanetElementDesign = ExoplanetElement(exoplanet.Radius, exoplanet.StellarRadius, StellarElementDesign.GetPixels(), earth.CONST_RADIUS, earth.CONST_STELLARRADIUS)

   #Rendering the results view with processed and parsed data relevant to the view
   if ChosenExoplanet:

       return render_template('results.html', 
        ChosenExoplanet = exoplanet.Name, 
        ExoplanetDetailsDictionary =  exoplanet.GetExoplanetDetailsDictionary(), 
        RelativeUserWeight = user.CalculateRelativeWeight(exoplanet.RelativeGravity),
        RelativeUserAge = user.CalculateRelativeAge(exoplanet.OrbitalPeriod),
        WeightType = user.WeightType, 
        ExoplanetSize = str(ExoplanetElementDesign.GetPixels()) + "px",
        ExoplanetColour = ExoplanetElementDesign.GetColour(),
        StellarSize = str(StellarElementDesign.GetPixels()) + "px",
        StellarColour = StellarElementDesign.GetColour(),
        EarthSize = str(EarthElementDesign.GetPixels()) + "px",
        EarthColour = EarthElementDesign.GetColour(),
        SunSize = str(SunElementDesign.GetPixels()) + "px",
        SunColour = SunElementDesign.GetColour()
       )

   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

#Running the Flask instance
if __name__ == '__main__':
   app.run()