from dotenv import load_dotenv
import psycopg2
import os
import warnings

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

#Singleton Pattern
class DBWrite:
    _instance = None

    def __init__(self):

        if DBWrite._instance != None:
            raise Exception("%s is a Singleton object. It can only be instantiated once." % type(self).__name__)
        else:
            DBWrite._instance = self

        self.conn = DBConnectionString()
        self.conn_string = self.conn.GetConnectionString()
        self.conn = psycopg2.connect(self.conn_string)
        self.cursor = self.conn.cursor()

    def ClearHits(self):
        
        # Drop current table
        self.cursor.execute("DROP TABLE IF EXISTS Pexo_Hits;")

        # Create a table
        self.cursor.execute("CREATE TABLE Pexo_Hits (exoplanetname VARCHAR(100) PRIMARY KEY, hits INTEGER);")
        self.conn.commit()

    def LogHits(self, ExoplanetName):
       
        # Insert some data into the table
        self.cursor.execute("INSERT INTO Pexo_Hits (exoplanetname, hits) SELECT '" + ExoplanetName +"',0 WHERE NOT EXISTS (SELECT exoplanetname FROM Pexo_Hits WHERE exoplanetname = '" + ExoplanetName + "');")
        self.cursor.execute("UPDATE Pexo_Hits set hits = hits + 1 WHERE exoplanetname = '" + ExoplanetName +"';")
        self.conn.commit()

#object pool + singleton pattern 
class DBReadPool:

    _instance = None

    def __init__(self, size):

        if DBReadPool._instance != None:
            raise Exception("%s is a Singleton object. It can only be instantiated once." % type(self).__name__)
        else:
            DBReadPool._instance = self

        self.conn = DBConnectionString()
        self.conn_string = self.conn.GetConnectionString()
        self._reusableconnections = []

        for _ in range(size):
            self.conn = psycopg2.connect(self.conn_string)
            self._reusableconnections.append(self.conn.cursor())

    def acquire(self):
        return self._reusableconnections.pop()

    def release(self, reusable):
        self._reusableconnections.append(reusable)

class DBRead:

    def __init__(self):

        self.pool = DBReadPool(5)
        self.maxhits = 10

    def GetTopHits(self):
        
        self.conn = self.pool.acquire()
        self.conn.execute("SELECT * FROM Pexo_Hits ORDER BY hits desc LIMIT %s"% self.maxhits)
        self.tophits= self.conn.fetchall()
        self.pool.release(self.conn)

        return self.tophits
    
# cursor.close()
# conn.close()