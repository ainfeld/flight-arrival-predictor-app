import traceback
from datetime import datetime as dt
from struct import pack, unpack
from flask import render_template, request, redirect, url_for
import logging.config
from src.add_flights import Flights
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pickle
from src.modeling import make_prediction
import pandas as pd
import argparse
import sys


# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Set up logging
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])

# Load trained model object
try:
    model = pickle.load(open(app.config["APP_MODEL"], 'rb'))
except FileNotFoundError:
    logger.error('The path to the trained model is not found.')
    sys.exit(1)

def inputs_conversion(date, dep, arr):
    month = date.month
    day = date.day
    weekday = date.weekday() + 1
    
    # extract hour blocks
    dep = dep.hour
    arr = arr.hour

    return month, day, weekday, dep, arr

def time_category(hour_var):
    if (hour_var >= 5) & (hour_var <= 11):
        output = 'Morning'
    elif (hour_var >= 12) & (hour_var <= 19):
        output = 'Afternoon/Evening'
    elif (hour_var <=4) | (hour_var >= 20):
        output = 'Night'
    return output


# Initialize the database
db = SQLAlchemy(app)

@app.route('/')
def index():
    """Main view where user puts in flight information

    Returns: rendered html template
    """
    logger.info('Load introductory page.')
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_inputs():
    """ Take in inputs user fills out 

    Make flight delay prediction and post prediction to the page 

    Returns: rendered html template
    """

    # evaluate user inputs
    date = request.form['date']
    try:
        std_date = dt.strptime(date, '%m/%d/%Y') 
    except ValueError:
        string = 'Enter a valid date format (mm/dd/yyyy).'
        logger.error(string)
        return render_template('index.html', message=string)

    airline = request.form['airline']
    if airline not in ['AA', 'B6', 'DL', 'UA', 'WN']:
        string = 'Invalid airline code. Please choose one of the following: AA, B6, DL, UA, WN'
        logger.error('Invalid airline. Please choose one of the following: AA, B6, DL, UA, WN')
        return render_template('index.html', message=string)

    origin = request.form['origin']
    dest = request.form['dest']
    if (len(origin) != 3) | (len(dest) != 3):
        string = 'Invalid airport code'
        logger.error(string)
        return render_template('index.html', message=string) 

    dep = request.form['dep_time']
    arr = request.form['arr_time']
    try:
        dep_time = dt.strptime(dep, '%H:%M')
        arr_time = dt.strptime(arr, '%H:%M')
    except ValueError:
        string = 'Enter a valid time format (hh:mm), 24 hour.'
        logger.error(string)
        return render_template('index.html', message=string)

    ## compile model inputs
    # extract date information
    Month, DayofMonth, DayOfWeek, DepTime_blk, ArrTime_blk = inputs_conversion(std_date, dep_time, arr_time)

    try:
        origin_week = db.session.query(Flights).filter_by(airline_label=airline, dayofweek=DayOfWeek, origin_label=origin).first()
    except:
        traceback.print_exc()
        logger.warning("Not able to query table")
        return render_template('error.html')
    try:
        Reporting_Airline = len(origin_week.airline)
        Origin = len(origin_week.origin)
        avg_org_day_airline = origin_week.avg_org_day
        f_int_origin = origin_week.f_int_origin
    except AttributeError:
        string = '{} airline does not fly out of {} on this day of the week.'.format(airline, origin)
        logger.error(string)
        return render_template('index.html', message=string)
    except:
        return render_template('error.html')

    # determine time category 
    DepTime_cat = time_category(DepTime_blk)
    ArrTime_cat = time_category(ArrTime_blk)

    try:
        origin_time = db.session.query(Flights).filter_by(airline_label=airline, deptime_cat=DepTime_cat, origin_label=origin).first()
    except:
        traceback.print_exc()
        logger.warning("Not able to query table")
        return render_template('error.html')
    try:
        avg_org_time_airline = origin_time.avg_org_time
    except AttributeError:
        string = '{} airline does not fly out of {} at this time.'.format(airline, origin)
        logger.error(string)
        return render_template('index.html', message=string)
    except:
        return render_template('error.html')
    try:
        dest_time = db.session.query(Flights).filter_by(airline_label=airline, arrtime_cat=ArrTime_cat, dest_label=origin).first()
    except:
        traceback.print_exc()
        logger.warning("Not able to query table")
        return render_template('error.html')
    try:
        Dest = len(dest_time.dest)
        avg_dest_time_airline = dest_time.avg_dest_time
        f_int_dest = dest_time.f_int_dest
    except AttributeError:
        string = '{} airline does not fly into to {} at this time.'.format(airline, dest)
        logger.error(string)
        return render_template('index.html', message=string)
    except:
        return render_template('error.html')

    new = {'Month':Month, 'DayofMonth': DayofMonth, 'DayOfWeek': DayOfWeek, 'Reporting_Airline':Reporting_Airline, 
           'Origin':Origin, 'Dest':Dest, 'DepTime_blk':DepTime_blk, 'ArrTime_blk':ArrTime_blk, 
           'avg_org_day_airline':avg_org_day_airline, 'avg_org_time_airline':avg_org_time_airline, 
           'avg_dest_time_airline':avg_dest_time_airline, 'f_int_origin':f_int_origin, 'f_int_dest':f_int_dest}
    new_df = pd.DataFrame(data=new, index = [0])

    try:
        prediction = make_prediction(model, new_df)
    except:
        return render_template('error.html')
    else:
        if prediction[0] == 2:
            string = 'Congrats! Looks like your flight will arrive on time!'
        elif prediciton[0] == 1:
            string = 'Oh no! Looks like your flight will be delayed getting in'
        else:
            string = 'Lucky! Looks like your flight will arrive early'
        logger.info('Result: {}'.format(string))
        return render_template('results.html', result=string)

if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])