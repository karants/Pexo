import psycopg2
import os

# Update connection string information

host = os.environ['HOST']
dbname = os.environ['DBNAME']
user = os.environ['USER']
password = os.environ['PASSWORD']
sslmode = "require"

# Construct connection string

conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)
print("Connection established")

cursor = conn.cursor()

# Drop previous table of same name if one exists

cursor.execute("DROP TABLE IF EXISTS exoplanets;")
print("Finished dropping table (if existed)")

# Create a table

cursor.execute("CREATE TABLE exoplanets (id serial PRIMARY KEY, planetname VARCHAR(50), yearofdiscovery INTEGER);")
print("Finished creating table")

# Insert some data into the table

cursor.execute("INSERT INTO exoplanets (planetname, yearofdiscovery) VALUES (%s, %s);", ("K2-365 b", 2022))
cursor.execute("INSERT INTO exoplanets (planetname, yearofdiscovery) VALUES (%s, %s);", ("K2-395 c", 2022))
cursor.execute("INSERT INTO exoplanets (planetname, yearofdiscovery) VALUES (%s, %s);", ("Kepler-1656 c", 2022))
print("Inserted 3 rows of data")

# Clean up

conn.commit()
cursor.close()
conn.close()