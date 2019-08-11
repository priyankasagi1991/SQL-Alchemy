import numpy as np
import pandas as pd
import sqlalchemy
import datetime as dt
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, inspect, func
from flask import Flask, jsonify

#create engine to connect with sqlite database
engine = create_engine("sqlite:///Homework_10-Advanced-Data-Storage-and-Retrieval_Instructions_Resources_hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)
#Using automap
Base = automap_base()
# reflecting tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes


@app.route("/")
def welcome():
    return jsonify({"Title":"Welcome to Hawaiin weather information","description": "This gives information about Hawaiin       stations precipitation and temperature values in a trip's date range","endpoints":["/api/v1.0/precipitation","/api/v1.0/stations","/api/v1.0/tobs","/api/v1.0/<start>","/api/v1.0/<start>/<end>"]})
                   
                    
           
    
@app.route("/api/v1.0/precipitation")

def precipitation():  
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Get the first element of the tuple
    latest_date = latest_date[0]

    # Calculate the date 1 year ago 
    # The days are equal 366 so that the first day of the year is included
    year_ago = dt.datetime.strptime(latest_date, "%Y-%m-%d") - dt.timedelta(days=366)
    
    # Perform a query to retrieve the data and precipitation scores
    date_prcp_scores= session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    precipitation_values= dict(date_prcp_scores)

    return jsonify(precipitation_values)

    
    
@app.route("/api/v1.0/stations")
def stations(): 
    stations =  session.query(Measurement.station).group_by(Measurement.station).all()

    stations_list = list(np.ravel(stations))

    return jsonify(stations_list)



@app.route("/api/v1.0/tobs")
def tobs(): 
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Get the first element of the tuple
    latest_date = latest_date[0]

    # Calculate the date 1 year ago from today
    # The days are equal 366 so that the first day of the year is included
    year_ago = dt.datetime.strptime(latest_date, "%Y-%m-%d") - dt.timedelta(days=366)
    # Query tobs
    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_ago).all()

    # Converting list of tuples into a list
    tobs_list = list(tobs)

    return jsonify(tobs_list)



@app.route("/api/v1.0/<start>")
def start(start=None):
    start_only_temp = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    start_only_temp_list=list(start_only_temp)
    return jsonify(start_only_temp_list)

    

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    start_end_temp = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    start_end_temp_list=list(start_end_temp )
    return jsonify(start_end_temp_list)



if __name__ == '__main__':
    app.run(debug=True)

    