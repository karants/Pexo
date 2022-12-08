from requests import Request, Session
import json

class ExoplanetAPI:

    def __init__(self):

        #API Host Endpoint
        self.APIHost = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
        self.APITableName = "ps"
        self.ResponseFormat = "json"

    def GetResponse(self, APIQuery):

        #Define Variables
        self.APIquery = APIQuery

         #Define the API Request
        self.CallParameters = {'query': self.APIquery, 'format': self.ResponseFormat}
        self.Request = Request('GET',self.APIHost, params = self.CallParameters)

        #Prepare the request and replace encoded characters with literals, as expected by the API
        self.PreparedRequest = self.Request.prepare()
        self.PreparedRequest.url = (self.PreparedRequest.url).replace("%2B","+")

        #Create session, send the query, store the response and close the session
        self.Session = Session()
        self.Response = self.Session.send(self.PreparedRequest)
        self.Session.close()

        #Convert the response content to Json
        self.ResponseData = json.loads(self.Response.content)

        return self.ResponseData


    def GetExoplanetsList(self):

        #Initialize Array Variables
        self.Exoplanets = []
        self.Keys = []

        #Define the query to obtain a list of exoplanets - abstracted from client code, creating a facade
        #Only obtain names (pl_name) of exoplanets with confirmed status 
        #and with recorded planetary mass (pl_masse), planetary radius (pl_rade) and stellar radius (st_rade)
        self.APIquery = "select+pl_name+from+"+self.APITableName+"+where+pl_masse+>+0+and+pl_rade+>+0+and+lower(soltype)+like+'%confirmed%'"

        #Get Response from the API and Parse the Response
        self.APIResponse=self.GetResponse(self.APIquery)
      
        for self.Row in self.APIResponse:
            for self.Key in self.Row.values():
                self.Keys.append(self.Key)

        #Remove duplicate entries from the Keys array
        self.Exoplanets = (list(dict.fromkeys(self.Keys)))

        return self.Exoplanets
   
    def GetExoplanetDetails(self, ChosenExoplanet):

        self.ChosenExoplanet = ChosenExoplanet

        self.RequiredFields = "pl_name,pl_masse,pl_rade,st_rad,sy_dist,pl_orbper,disc_year,disc_facility,discoverymethod,disc_pubdate,pl_pubdate"

        self.APIquery = "select+" +self.RequiredFields+ "+from+"+self.APITableName+"+where+pl_name+=+'"+self.ChosenExoplanet+ "'+and+pl_masse+>+0+and+pl_rade+>+0+order+by+pl_pubdate+desc"

        #Get Response from the API
        self.APIResponse=self.GetResponse(self.APIquery)

        #First dictionary in the array contains the response
        ExoplanetDetails=self.APIResponse[0]

        return ExoplanetDetails