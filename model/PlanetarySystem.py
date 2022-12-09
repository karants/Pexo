#This is a model implementation named Planetary System. Could not find a way to implement a design pattern.
# Would love to hear how this can be better implemented.
#It has been called Planetary system, in case future iterations include analysis on the Stellar host or Moons that orbit around the exoplanet.
#Currently, creating only the planet object

#Author: Karan Shah
#Contact: shahk47@mcmaster.ca

#Import Pip Libraries
from abc import ABC, abstractmethod
import math

class Planet(ABC):

    CONST_PascalToLightYear = 3.26156

    @abstractmethod
    def __init__(self):
        pass

class Exoplanet(Planet):

    def __init__(self,PlanetaryDetails):

        #Planetary Details are obtained by the controller from the ExoplanetAPI model. 
        self.PlanetaryDetails = PlanetaryDetails
        self.Name = self.PlanetaryDetails['pl_name']
        self.Mass = self.PlanetaryDetails['pl_masse']
        self.Radius = self.PlanetaryDetails['pl_rade']
        self.OrbitalPeriod = round(self.PlanetaryDetails['pl_orbper'])
        self.DiscoveryYear = self.PlanetaryDetails['disc_year']
        self.DiscoveryFacility = self.PlanetaryDetails['disc_facility']
        self.DiscoveryMethod = self.PlanetaryDetails['discoverymethod']
        self.DistanceFromEarth = round(self.PlanetaryDetails['sy_dist'] * super().CONST_PascalToLightYear)
        self.StellarRadius = self.PlanetaryDetails['st_rad']
        self.RelativeGravity = ((float(self.Mass)/float(math.pow(self.Radius,2)))) #relative gravity = relative mass/square of relative radius

    #This is solely created to be consumed by the View. Thought about using an Adapter Pattern but couldn't figure out how best that would work.
    def GetExoplanetDetailsDictionary(self):

        self.ExoplanetDetails = {
            "Name": self.Name,
            "Mass": self.Mass,
            "Radius": self.Radius,
            "OrbitalPeriod": self.OrbitalPeriod,
            "DiscoveryYear": self.DiscoveryYear,
            "DiscoveryFacility": self.DiscoveryFacility,
            "DiscoveryMethod": self.DiscoveryMethod,
            "DistanceFromEarth": self.DistanceFromEarth,
            "StellarRadius": self.StellarRadius,
            "RelativeGravity": self.RelativeGravity
        }
        
        return self.ExoplanetDetails

#Pretty much constant variables, no functions for now.
class Earth(Planet):

    def __init__(self):

        self.CONST_NAME = "Earth"
        self.CONST_GRAVITY = 9.81
        self.CONST_RADIUS = 6378
        self.CONST_STELLARRADIUS = 696265