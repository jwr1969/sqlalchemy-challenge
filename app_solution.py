#################################################
# Python SQL toolkit and Object Relational Mapper
#################################################
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt
from dateutil.parser import parse
# Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine,reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station
#################################################
from flask import Flask, jsonify
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>" 
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start%20date<br/>"
        f"/api/v1.0/start%20date/end%20date<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation_data():
    """Return the precipitation data as json"""
    session = Session(engine)
    # Determine last date (most recent) in measurement table
    last_date = session.query(func.max(measurement.date)).first()
    print(last_date)
    # Parse date into datetime object
    last_date_dt = dt.datetime.strptime(last_date[0],'%Y-%m-%d')
    print(last_date_dt)
    # Calculate the date 1 year ago from the last data point in the database
    # Precipitation (across all 9 measurement stations) for each day of the most recent year
    results = session.query(measurement.date,measurement.prcp).\
    filter(measurement.date > (last_date_dt  - dt.timedelta(days=366))).all()
    precipitation = {result[0]:result[1] for result in results}

    session.close()

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    """Return the station names as json"""

    # open session
    session = Session(engine)
    # database query
    stations_names = session.query(measurement.station).distinct().all()
    # list comprehension to enable data for jsonify
    stations_names_list = [name[0] for name in stations_names]
    # close session
    session.close()
    
    return jsonify(stations_names_list)        

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperatures as json"""
    # open session
    session = Session(engine)
    # last / most recent date from dataset
    last_date = session.query(func.max(measurement.date)).first()
    last_date_dt = dt.datetime.strptime(last_date[0],'%Y-%m-%d')
    # database query for find most active station
    most_active_station = session.query(measurement.station).group_by(measurement.station).\
    order_by(func.count(measurement.id).desc()).first()[0]
    # database query to temperatures using most active station as filter
    temp_from_most_active = session.query(measurement.date, measurement.tobs).\
    filter(measurement.station==most_active_station).\
    filter(measurement.date > (last_date_dt  - dt.timedelta(days=366))).all()
    # dict comprehension to enable data for jsonify
    most_active_station_dict = {result[0]:result[1] for result in temp_from_most_active}
    # close session
    session.close()

    return jsonify(most_active_station_dict)

@app.route("/api/v1.0/<start_date>")
def start(start_date):
    """Return minimum temperature, the average temperature, 
    and the max temperature for for all dates greater than 
    and equal to the start date"""
    # convert the input dates into a standard format
    canonicalized = dt.datetime.strftime(parse(start_date), '%Y-%m-%d')
    # open session
    canonicalized = dt.datetime.strftime(parse(start_date), '%Y-%m-%d')
    session = Session(engine)
    # database query
    output = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= canonicalized).all()
    # close session
    session.close()
    # put outputs into a form user can understand!
    text = f"For the date range from {canonicalized} onwards: Tmax= {output[0][2]}F, Tavg= {round(output[0][1],1)}F and Tmin= {output[0][0]}F"

    return jsonify(text)

@app.route("/api/v1.0/<start_date>/<end_date>")
def end(start_date,end_date):
    """Return the minimum temperature, the average temperature, 
    and the max temperature for all dates between the start and end date inclusive"""

    # convert the input dates into a standard format   
    canonicalized_start = dt.datetime.strftime(parse(start_date),"%Y-%m-%d")
    canonicalized_end = dt.datetime.strftime(parse(end_date),"%Y-%m-%d")
    # open session
    session = Session(engine)
    # database query
    output = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= canonicalized_start).filter(measurement.date <= canonicalized_end).all()
    # close session
    session.close()
    # put outputs into a form user can understand!
    text = f"For the date range from {canonicalized_start} to {canonicalized_end}: Tmax= {output[0][2]}F, Tavg= {round(output[0][1],1)}F and Tmin= {output[0][0]}F"
    return jsonify(text)


if __name__ == "__main__":
    app.run(debug=True)
