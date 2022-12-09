#This is a model implementation named User Details. It consumes user input and exoplanet related data to produce relative information for the User.

#Author: Karan Shah
#Contact: shahk47@mcmaster.ca

#Import Pip libraries
from datetime import datetime, date

class User:
    
    def __init__(self, weight, weighttype, birthday):

        self.Weight = weight
        self.WeightType = weighttype
        self.Birthday = birthday
        
    def CalculateRelativeWeight(self, ChosenExoplanetRelativeGravity):

        self.ChosenExoplanetRelativeGravity = ChosenExoplanetRelativeGravity

        #relative weight calculation: Weight on Exoplanet = Weight on Earth x Exoplanet's Relative Gravity
        self.RelativeWeight = ((float(self.Weight)) * self.ChosenExoplanetRelativeGravity)

        return round(self.RelativeWeight)

    def CalculateRelativeAge(self, ChosenExoplanetOrbitalPeriod):

        self.ChosenExoplanetOrbitalPeriod = ChosenExoplanetOrbitalPeriod

        #relative age calculation: relative age = number of days on Earth / orbital period of the exoplanet
        self.RelativeAge = ((datetime.today() - datetime.strptime(self.Birthday,'%Y-%m-%d')).days / self.ChosenExoplanetOrbitalPeriod)

        return round(self.RelativeAge)