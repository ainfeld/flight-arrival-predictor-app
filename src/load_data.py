from os import path
import sys
import argparse
import logging

import pandas as pd
import yaml

from src.helpers import get_file_names, load_file, subset

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger('clean_data')

def load_flight_data(df, variable, airlines, columns):
    """ Load raw data file and limit to raw observations in scope
    Args:
        df (dataframe): dataframe of raw data from file
        variable (str): column used to subset the data
        airlines (list): list of airlines to include observations in the dataset
        columns (list): list of relevant columns to include in the dataset
    Returns: 
        df (dataframe): subset dataframe of data in scope
    """
    # limit to top 5 airlines
    if type(airlines) != list:
        airlines = [airlines]
    try:
        df = df[df[variable].isin(airlines)]
    except KeyError:
        logger.error('Column {} does not exist.'.format(variable))
    else:
    # confirm included airlines
        included_airlines = list(df[variable].unique())
        expected_airlines = ['AA', 'B6', 'DL', 'UA', 'WN']
        if set(included_airlines) != set(expected_airlines):
            logger.warning('After subsetting to the top 5 airlines, not all expected airlines are included in this set.')
            missing = list(set(expected_airlines) - set(included_airlines))
            logger.debug('The following airlines were expected but not included: {}'.format(missing))
    # limit to relevant variables
    if type(columns) != list:
        columns = [columns]
    df = subset(df, columns)
    
    # confirm included columns
    included_columns = list(df.columns)
    expected_columns = ['FlightDate','Year','Month', 'DayofMonth', 'DayOfWeek','Reporting_Airline', 
                        'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime','ArrDelay', 'Cancelled', 'Diverted', 
                        'Flights']
    if set(included_columns) != set(expected_columns):
        logger.warning('Not all expected columns are included in this set.')
        logger.debug('Included columns: {}'.format(included_columns))

    return df

def combine_flight_data(s3_local_path, file_list, variable, airlines, columns):
    """ Combines all flight files into one dataset
    Args:
        s3_local_path (str): path to directory of files downloaded from S3
        file_list (str): List of file names
        variable (str): column used to subset the data
        airlines (list): list of airlines to include observations in the dataset
        columns (list): list of relevant columns to include in the dataset
    Returns:
        df (dataframe): dataframe of full airline delay data set
    """
    flight_data = []
    for file in file_list: 
        local_flight_path = s3_local_path + file
        df = load_file(path = local_flight_path, file_type = 'csv')
        df = load_flight_data(df = df, variable = variable, airlines = airlines, columns = columns)
        flight_data.append(df)

    logger.info('There were {} files successfully loaded.'.format(len(flight_data)))

    try:
        df = pd.concat(flight_data, axis=0, ignore_index=True)
        return df
    except ValueError:
        logger.error('There is no flight data to concatenate.')

    

def run_load_data(config_path, s3_local_path, raw_path):
    """ Combine all flight data files
    Args:
        config_path (str): path to yaml configuration file
        s3_local_path (str): path to directory of files downloaded from S3
        raw_path (str): path to file raw version of the data should be stored 
    Returns:
        df (dataframe): dataframe of full dataset 
    """
    try:
        with open(config_path, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            config = config['load_data']
    except FileNotFoundError:
        logger.error('The following file was not found: {} \n Please provide a valid path to the configuration file.'.format(config_path))
        sys.exit(1)

    # Get list of filenames of files to read in 
    try:
        file_list = get_file_names(dir_path = s3_local_path, ext = ".csv")
    except FileNotFoundError:
        logger.error("Directory not found. Please provide a valid directory location to extract file names.")
        sys.exit(1)

    logger.info("There were {} file names retrieved.".format(len(file_list)))

    # combine flight data
    df = combine_flight_data(s3_local_path = s3_local_path, file_list = file_list, **config['load_flight_data'])

    # save data to csv
    try:
        df.to_csv(raw_path, index = False)
        logger.info('Combined raw data was written to {}'.format(raw_path))
    except FileNotFoundError:
        logger.error('The path to save this file does not exist.')
        sys.exit(1)
    except AttributeError:
        logger.error('There is no data to save out.')
    except NameError:
        logger.error('There is no data to save out.')

    

