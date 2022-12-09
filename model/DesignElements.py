#This is a model implementation named Design Element. It is implemented using the Template Method Pattern - Behavioral Design Pattern.
#The DesignElementTemplate class is the abstract class that plays the role of a template, whereas the other classes are concrete subclasses
#Efforts were made to make this a hybrid Factory design pattern but it proved to be not worthwhile the effort as it would increase the complexity of the design

#Author: Karan Shah
#Contact: shahk47@mcmaster.ca

#Importing Pip Libraries
from abc import ABC, abstractmethod

#Define abstract base class in the Template Method Pattern
class DesignElementTemplate(ABC):

    #This is a class variable that defines the size (in pixels) of all the Host star elements
    HostStarSize = 500

    #abstract method to get the number of pixels of an element
    @abstractmethod
    def GetPixels(self):
        pass

    #abstract method to get the colour of an element
    @abstractmethod
    def GetColour(self):
        pass

#Subclass to define the Earth Element with inheritance from the template
class EarthElement(DesignElementTemplate):

    def __init__(self, EarthRadius, SunRadius, SunPixels):

        self.EarthRadius = EarthRadius
        self.SunRadius = SunRadius
        self.SunPixels = SunPixels
        
    def GetPixels(self):

        #The ratio of sun's radius and earth radius is mapped to pixels
        self.EarthPixels = (self.SunPixels / ((self.SunRadius / self.EarthRadius)))

        return round(self.EarthPixels, 2)

    def GetColour(self):

        return "#1A3D61"

#Subclass to define the Sun Element with inheritance from the template
class SunElement(DesignElementTemplate):

    def GetPixels(self):
        return super().HostStarSize #Defined in base template
    
    def GetColour(self):
        return "#DE9700"

#Subclass to define the Exoplanet Element with inheritance from the template
class ExoplanetElement(DesignElementTemplate):

    def __init__(self, PlanetRadius, StellarRadius, StellarPixels, EarthRadius, SunRadius):

        self.PlanetRadius = PlanetRadius
        self.StellarRadius = StellarRadius
        self.StellarPixels = StellarPixels
        self.EarthRadius = EarthRadius
        self.SunRadius = SunRadius

    def GetPixels(self):

        #Exoplanet Radius obtained from the API is a multiple of Earth's radius and the Stellar radius is a multiple of Sun's radius
        #To obtain the size ratio of the Exoplanet vs it's Stellar Host, both have to be multiplied to Earth's Radius and Sun's radius respectively
        self.PlanetPixels = (self.StellarPixels / (((self.StellarRadius * self.SunRadius) / (self.PlanetRadius * self.EarthRadius))))

        return round(self.PlanetPixels, 2)

    def GetColour(self):

        return "#3C6795"

#Subclass to define the Stellar Element with inheritance from the template
class StellarElement(DesignElementTemplate):

    def GetPixels(self):
        return super().HostStarSize #Defined in base template

    def GetColour(self):
        return "#FFAE00"