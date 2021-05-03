#! /usr/bin/python3

"""
ONE-TIME SETUP

To run this example in the CSC 315 VM you first need to make
the following one-time configuration changes:

# set the postgreSQL password for user 'lion'
sudo -u postgres psql
    ALTER USER lion PASSWORD 'lion';
    \q

# install pip for Python 3
sudo apt update
sudo apt install python3-pip

# install psycopg2
pip3 install psycopg2-binary

# install flask
pip3 install flask

# logout, then login again to inherit new shell environment
"""

"""
CSC 315
Spring 2021
John DeGood

# usage
export FLASK_APP=app.py 
flask run

# then browse to http://127.0.0.1:5000/

Purpose:
Demonstrate Flask/Python to PostgreSQL using the psycopg adapter.
Connects to the 7dbs database from "Seven Databases in Seven Days"
in the CSC 315 VM.

For psycopg documentation:
https://www.psycopg.org/

This example code is derived from:
https://www.postgresqltutorial.com/postgresql-python/
https://scoutapm.com/blog/python-flask-tutorial-getting-started-with-flask
https://www.geeksforgeeks.org/python-using-for-loop-in-flask/
"""

import psycopg2
from config import config
from flask import Flask, render_template, request

def connect(query):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters from database.ini
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
      
        # create a cursor
        cur = conn.cursor()
        
        # execute a query using fetchall()
        cur.execute(query)
        rows = cur.fetchall()
        #colnames = [desc[0] for desc in cur.description]

       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows

def search(searchterm, search_by, sort_by):
    """ Connect to the PostgreSQL database server """
    conn = None
    query = ""
    try:
        # read connection parameters from database.ini
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
      
        # create a cursor
        cur = conn.cursor()
        
        # select what the query is based on dropdown
        if search_by == "title":
            query += "SELECT distinct AID, TITLE, INTERVIEW_DATE FROM SEARCHVIEW WHERE LOWER(title) LIKE \'%" + searchterm.lower()
        elif search_by == "participant":
            queryfirstname = "SELECT distinct AID, TITLE, INTERVIEW_DATE FROM SEARCHVIEW WHERE LOWER(first_name) LIKE \'%" + searchterm.lower() + "%\'"
            querylastname = "SELECT distinct AID, TITLE, INTERVIEW_DATE FROM SEARCHVIEW WHERE LOWER(last_name) LIKE \'%" + searchterm.lower() + "%\'"
            querymiddlename = "SELECT distinct AID, TITLE, INTERVIEW_DATE FROM SEARCHVIEW WHERE LOWER(middle_name) LIKE \'%" + searchterm.lower() + "%\'"
            query += queryfirstname + " UNION " + querylastname + " UNION " + querymiddlename
        
        elif search_by == "place":
            querycity = "SELECT distinct AID, TITLE, INTERVIEW_DATE FROM SEARCHVIEW WHERE LOWER(city) LIKE \'%" + searchterm.lower() + "%\'"
            querystate = "SELECT distinct AID, TITLE, INTERVIEW_DATE FROM SEARCHVIEW WHERE LOWER(state) LIKE \'%" + searchterm.lower() + "%\'"
            query += querycity + " UNION " + querystate

        else:
            pass

        if sort_by == "newest-to-oldest":
            query += " ORDER BY INTERVIEW_DATE DESC;"
        elif sort_by == "oldest-to-newest":
            query += " ORDER BY INTERVIEW_DATE ASC;"
        else:
            pass


        # execute a query using fetchall()
        # query = "SELECT * FROM ARCHIVES WHERE LOWER(title) LIKE \'%" + searchterm.lower() + "%\';"
        # cur.execute(query)
        
        cur.execute(query)
        rows = cur.fetchall()
        #colnames = [desc[0] for desc in cur.description]

       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows
 
# app.py
app = Flask(__name__)


# serve form web page
@app.route("/")
def form():
    # handle form data
    return render_template('my-form.html')

@app.route('/form-handler', methods=['POST'])
def handle_data():
    rows = search(request.form['searchterm'], request.form['search_by'], request.form['sort_by'])
    return render_template('my-form.html', rows=rows)

@app.route("/archives/<id>")
def show(id):
    query = "SELECT * FROM MAINVIEW WHERE AID = " + id + "LIMIT 1;"
    row = connect(query)
    return render_template('my-result.html', row = row)

#handle login data
# @app.route('/login-handler', methods='POST')
# def handle_login():
#     return

if __name__ == '__main__':
    app.run(debug = True)
