import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
msrTbl = Base.classes.measurement
staTbl = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def names():
    """Return precipitation totals for 2010"""
    # 
    #select a year worth of precipitation
    qry = session.query(msrTbl.date, func.sum(msrTbl.prcp)).\
        filter(msrTbl.date.between('2010-01-01', '2010-12-31')).\
        group_by(msrTbl.date).all()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(qry))

    return jsonify(all_names)


@app.route("/api/v1.0/tobs")
def passengers():
    """Return a list of total observations by weather station"""
    # Query all stations and total obsersvations

    sel = [msrTbl.station, msrTbl.date, msrTbl.prcp, msrTbl.tobs, staTbl.elevation, staTbl.latitude, staTbl.longitude]
    results = session.query(*sel).filter(msrTbl.station == staTbl.station).all()
    
    results_df = pd.DataFrame(results, columns=['station', 'date','prcp', 'tobs','elevation','latitude','longitude'])
    results_df.set_index(results_df['date'], inplace=True)
    
    station_tobs = results_df.groupby('station')['tobs'].sum()

  # Create a dictionary from the row data and append to a list of all_passengers
    sta_list = ['USC00511918','USC00513117','USC00514830','USC00516128','USC00517948','USC00518838','USC00519281','USC00519397','USC00519523']

    tobs_list = []
    for x in range(len(sta_list)):
        tobs_dict = {}
        tobs_dict["station"] = sta_list[x]
        tobs_dict["tobs"] = str(station_tobs[x])
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

# @app.route("/api/v1.0/tobs")
# def passengers():
#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger).all()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for passenger in results:
#         passenger_dict = {}
#         passenger_dict["name"] = passenger.name
#         passenger_dict["age"] = passenger.age
#         passenger_dict["sex"] = passenger.sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)

# @app.route("/api/v1.0/tobs")
# def passengers():
#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger).all()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for passenger in results:
#         passenger_dict = {}
#         passenger_dict["name"] = passenger.name
#         passenger_dict["age"] = passenger.age
#         passenger_dict["sex"] = passenger.sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)

