import os
import psycopg2
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

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


@app.route('/')
def index():
   print('Request for index page received')
   cursor.execute('SELECT * FROM exoplanets;')
   exoplanets = cursor.fetchall()
   cursor.close()
   conn.close()
   return render_template('index.html', exoplanets=exoplanets)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()