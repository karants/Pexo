#This is a model implementation named DBconnection. It facilitates read and write capabilities with an SQL database.
#DBWrite is implemented using Singleton pattern to log data into the DB.
#DBRead is implemented using Object Pool Pattern. The DBReadPool acts as the Object Pool and is implemented as a Singleton.

#Author: Karan Shah
#Contact: shahk47@mcmaster.ca

#Importing Pip Libraries
from dotenv import load_dotenv
import psycopg2
import os

#Defining the connection string to the DB that can be utilized by multiple DB connection objects - reducing code duplication
class DBConnectionString:

    def __init__(self):
        
        #Load Env Variables and Construct Connection String
        load_dotenv()
        self.__host=os.getenv('HOST')
        self.__dbname = os.getenv('DBNAME')
        self.__user = os.getenv('USER')
        self.__password = os.getenv('PASSWORD')
        self.__sslmode = "require"
        self.__conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(self.__host, self.__user, self.__dbname, self.__password, self.__sslmode)

    def GetConnectionString(self):
        return self.__conn_string

#Singleton Pattern Implementation for Logging Data to the DB
class DBWrite:
    _instance = None

    def __init__(self):

        #Exception is raised when there is an attempt to instantiate the object more than once
        if DBWrite._instance != None:
            raise Exception("%s is a Singleton object. It can only be instantiated once." % type(self).__name__)
        else:
            DBWrite._instance = self

        #Connecting to the DB and obtaining the cursor
        self.conn = DBConnectionString()
        self.conn_string = self.conn.GetConnectionString()
        self.conn = psycopg2.connect(self.conn_string)
        self.cursor = self.conn.cursor()

    #Just in case there is a need to clear all the hits :) Not used actively.
    def ClearHits(self):
        
        # Drop the hits table
        self.cursor.execute("DROP TABLE IF EXISTS Pexo_Hits;")

        # Create the hits table. Exoplanetname works as primary key as the list is uniquely generated from the API call (ExoplanetAPI)
        self.cursor.execute("CREATE TABLE Pexo_Hits (exoplanetname VARCHAR(100) PRIMARY KEY, hits INTEGER);")
        self.conn.commit()

    def LogHits(self, ExoplanetName):
       
        # Inserting the exoplanet name if it does not exist into the hits table and updating the hits (current hits + 1)
        self.cursor.execute("INSERT INTO Pexo_Hits (exoplanetname, hits) SELECT '" + ExoplanetName +"',0 WHERE NOT EXISTS (SELECT exoplanetname FROM Pexo_Hits WHERE exoplanetname = '" + ExoplanetName + "');")
        self.cursor.execute("UPDATE Pexo_Hits set hits = hits + 1 WHERE exoplanetname = '" + ExoplanetName +"';")
        self.conn.commit()

#object pool + singleton pattern  implementation
class DBReadPool:

    _instance = None

    def __init__(self, size):

        if DBReadPool._instance != None:
            raise Exception("%s is a Singleton object. It can only be instantiated once." % type(self).__name__)
        else:
            DBReadPool._instance = self

        self.conn = DBConnectionString()
        self.conn_string = self.conn.GetConnectionString()

        #array for the pool
        self._reusableconnections = []

        #filling up the pool with DB connections
        for _ in range(size):
            self.conn = psycopg2.connect(self.conn_string)
            self._reusableconnections.append(self.conn.cursor())

    #Function to acquire a DB connection
    def acquire(self):
        return self._reusableconnections.pop()

    #Function to release a DB connection
    def release(self, reusable):
        self._reusableconnections.append(reusable)


#Executing DB read functions
class DBRead:

    def __init__(self):

        #instantiating the pool with a size
        self.pool = DBReadPool(5)
        #defining the number of total number hits to obtain
        self.maxhits = 10

    #Function to get the top hits from the hits table
    def GetTopHits(self):
        
        self.conn = self.pool.acquire()
        self.conn.execute("SELECT * FROM Pexo_Hits ORDER BY hits desc LIMIT %s"% self.maxhits)
        self.hits= self.conn.fetchall()
        self.pool.release(self.conn)
        self.tophits = [self.hits[_][0] for _ in range(len(self.hits))]

        #returning array of exoplanet names
        return self.tophits