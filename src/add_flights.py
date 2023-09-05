import os
import sys
import logging
import logging.config
import argparse

import yaml

from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sql

from src.helpers import load_file, subset
from src.modeling import convert_categorical 

import config

Base = declarative_base() 

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger("create_db")

class Flights(Base):
    """ Defines the data model for the table `flights`. """
    __tablename__ = 'flights'

    flight_id = Column(Integer, primary_key=True)
    airline = Column(LargeBinary, unique = False, nullable = False)
    airline_label = Column(String(100), unique = False, nullable = False)
    dayofweek = Column(Float, unique = False, nullable = False)
    origin = Column(LargeBinary, unique = False, nullable = False)
    origin_label = Column(String(100), unique = False, nullable = False)
    dest = Column(LargeBinary, unique = False, nullable = False)
    dest_label = Column(String(100), unique = False, nullable = False)
    deptime_cat = Column(String(100), unique = False, nullable = False)
    arrtime_cat = Column(String(100), unique = False, nullable = False)
    avg_org_day = Column(Float, unique = False, nullable = False)
    avg_org_time = Column(Float, unique = False, nullable = False)
    avg_dest_time = Column(Float, unique = False, nullable = False)
    f_int_origin = Column(Integer, unique = False, nullable = False)
    f_int_dest = Column(Integer, unique = False, nullable = False)

    def __repr__(self):
        flight_record = "<Flights(flight_id = '%d', airline = '%d', airline_label = '%s', dayofweek = '%d', origin ='%d', origin_label = '%s', dest = '%d', dest_label = '%s', deptime_cat = '%s', arrtime_cat = '%s', avg_org_day = '%.2f', avg_org_time = '%.2f', avg_dest_time = '%.2f', 'f_int_origin' = '%d', f_int_dest' = '%d')>"
        return flight_record % (self.flight_id, self.airline, self.airline_label, self.dayofweek, self.origin, self.origin_label, self.dest, self.dest_label, self.deptime_cat, self.arrtime_cat, self.avg_org_day, self.avg_org_time, self.avg_dest_time, self.f_int_origin, self.f_int_dest)

def create_db(engine_string):
    """Creates a database with the data models inherited from `Base` (Flights).
    Args:
        engine_string (str): String defining SQLAlchemy connection URI
    Returns:
        engine (sqlalchemy.engine.Engine): SQLAlchemy connection engine
    """
    # create connection
    try:
        engine = sql.create_engine(engine_string)
        logger.info('Connection to database was made successfully.')
    except:
        logger.error('Failed connection to database.')

    try:
        Base.metadata.create_all(engine)
        logger.info('Table in database was created.')
        return engine
    except:
        logger.error('Failed creation of table in database.')
            

def translation_table(processed_path, columns, categories, float_columns):
    """ Create translation table to determine model inputs 
    Args:
        processed_path (str): path to processed data
        columns (list): list of columns to include in table
        categories (list): list of columns to make categorical 
        float_columns (str): name of columns to turn to float
    Returns:
        df (dataframe): dataframe of set to add to SQL database
    """

    # load processed data 
    df = load_file(path = processed_path, file_type = 'csv')

    # limit to relevant variables
    if type(columns) != list:
        columns = [columns]
    df = subset(df, columns)

    if type(categories) != list:
        categories = [categories]

    for cat in categories: 
        new = cat + '_label'
        if new in list(df.columns):
            logger.warning('Column {} is about to be overwritten.'.format(new))
        try:
            df[new] = df[cat]
        except KeyError:
            logger.error('Column {} does not exist.'.format(cat))

    # convert certain variables categorical
    df = convert_categorical(df, categories)

    # convert to float
    for col in float_columns:
        try:
            df[col] = df[col].astype(object)
        except KeyError:
                logger.error('Column {} does not exist.'.format(col))
        except ValueError:
                logger.error('Column {} cannot be converted into a float.'.format(col))

    df = df.drop_duplicates()
    logger.info('Length of translation table: {}'.format(len(df)))
    return df

def persist_translation(df, engine):
    """ Persist scores into table `Flights` in database.
    Args:
        df (dataframe): translation table to add to database
        engine (sqlalchemy.engine.Engine): SQLAlchemy connection engine
    Returns:
        None
    """
    # start session 
    Session = sessionmaker(bind=engine)
    session = Session()

    # create record
    for i in range(len(df)):
        airline = df.Reporting_Airline.iloc[i]
        airline_label = df.Reporting_Airline_label.iloc[i]
        dayofweek = df.DayOfWeek.iloc[i]
        origin = df.Origin.iloc[i]
        origin_label = df.Origin_label.iloc[i]
        dest = df.Dest.iloc[i]
        dest_label = df.Dest_label.iloc[i]
        deptime_cat = df.DepTime_cat.iloc[i]
        arrtime_cat = df.ArrTime_cat.iloc[i]
        avg_org_day = df.avg_org_day_airline.iloc[i]
        avg_org_time = df.avg_org_time_airline.iloc[i]
        avg_dest_time = df.avg_dest_time_airline.iloc[i]
        f_int_origin = df.f_int_origin.iloc[i]
        f_int_dest = df.f_int_dest.iloc[i] 

        flight_record = Flights(airline = airline, airline_label = airline_label, dayofweek = dayofweek,
                                origin = origin, origin_label = origin_label, dest = dest, dest_label = dest_label, deptime_cat = deptime_cat, arrtime_cat = arrtime_cat, 
                                avg_org_day = avg_org_day, avg_org_time = avg_org_time, avg_dest_time = avg_dest_time, 
                                f_int_origin = f_int_origin, f_int_dest = f_int_dest)
        # add record to the database
        session.add(flight_record)
        if i%1000 == 0:
        	session.commit()
        	logger.debug('Commited up to {} records.'.format(i))

    # commit additions
    session.commit()
    session.close()

def set_up_db(config_path, processed_path, engine_string):
    """ Run database set up and configuration 
    Args:
        config_path (str): path to yaml configuration file
        processed_path (str): path of file with the processed version of the data
        engine_string (str): String defining SQLAlchemy connection URI
    Returns:
        None
    """
    # load yaml configuration file
    try:
        with open(config_path, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            config = config['flights_db']
    except FileNotFoundError:
        logger.error('The following file was not found: {} \n Please provide a valid path to the configuration file.'.format(config_path))
        sys.exit(1)

    # create database
    engine = create_db(engine_string)

    # create table
    df = translation_table(processed_path, **config['translation'])

    # persist translation table to database
    persist_translation(df, engine)


    
    
