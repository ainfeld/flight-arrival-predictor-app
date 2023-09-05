import sys
import argparse
import logging

import pandas as pd
import yaml

from src.helpers import get_file_names, load_file, subset

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger('generate_features')

def flag_international_airports(df, variable, columns, old, new):
    """ Create translation table that flags which airports service international flights
    Args:
        df (dataframe): pandas dataframe of airport dataset
        variable (str): new column that flags international airports
        columns (list): list of relevant columns
        old (str): original column name with airport codes
        new (str): column name in data for merging
    Returns:
        df (dataframe): dataframe of airport translation table
    """
    # add flag
    try: 
        df[variable] = 1
    except KeyError:
        logger.error('Column {} does not exist.'.format(variable))

    df = subset(df = df, columns = columns)

    # rename column
    try:
        if new in list(df.columns):
            logger.warning('{} column already exists. It will be overwritten.'.format(new))
        df = df.rename(columns={old : new})
    except KeyError:
        logger.error('Column {} does not exist.'.format(old))

    return df
def convert_str(df, variable):
    """ Convert variable in dataframe to type string
    Args:
        df (dataframe): pandas dataframe of dataset
        column (str): name of column to convert to string
    Returns:
        df (dataframe): dataframe with column as type string
    """
    try: # attempt to convert column to type string
        df[variable] = df[variable].astype(str)
    except KeyError:
        logger.error('Column {} does not exist.'.format(variable))
    return df 

def calculate_flight_averages(df, sum_columns, avg_columns, new):
    """ Calculate averages number of flights for each combination of specific variables 
    Args:
        df (dataframe): pandas dataframe of dataset
        sum_columns (list): list of columns to sum number of flights over 
        avg_columns (list): list of columns to average number of flights over 
        new (str): name of new average variable
    Returns: 
        df (dataframe): dataframe of average column and variables flights were averaged over 
    """
    try: # sum flights over columns
        df = df.groupby(sum_columns).sum().reset_index()
    except KeyError:
        logger.error('One or more columns do not exist: {}'.format(sum_columns))
    try: # average flights over columns
        df = df.groupby(avg_columns).mean().reset_index()
    except KeyError:
        logger.error('One or more columns do not exist: {}'.format(avg_columns))
    if new in list(df.columns):
        logger.warning('{} column already exists. It will be overwritten.'.format(new))
    df = df.rename(columns={'Flights':new})

    return df

def merge_features(df, subset, method, columns, old = None, new = None):
    """ Merge dataframes 
    Args:
        df (dataframe): dataframe of full dataset
        subset (dataframe): dataframe with additional features
        method (str): type of merge 
        columns (list): columns to merge on
        old (str): variable to rename 
        new (str): new name of variable
    Returns: 
        df (dataframe): dataframe with additional features
    """
    if type(columns) != list:
        columns = [columns]

    try: # attempt to merge dataframes 
        df = pd.merge(df, subset, how = method, on = columns)
    except KeyError:
        logger.error('One or more columns do not exist: {}'.format(columns))

    # rename variables
    if new is not None: 
        df = df.rename(columns = {old : new})
        df[new].fillna(value = 0, inplace = True)

    return df

def run_generate_features(config_path, cleaned_path, s3_local_path, processed_path):
    """ Run generate features script
    Args:
        config_path (str): path to yaml configuration file
        cleaned_path (str): path to file cleaned version of the data was stored
        airport_path (str): path to file with international airport data
        processed_path (str): path to file processed version of the data should be stored
    Returns:
        None
    """
    # load yaml configuration file
    try:
        with open(config_path, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            config = config['generate_features']
    except FileNotFoundError:
        logger.error('The following file was not found: {} \n Please provide a valid path to the configuration file.'.format(config_path))
        sys.exit(1)

    # flag international airports
    logger.info('Creating international airport translation tables')

    # get file name 
    try:
        file_list = get_file_names(dir_path = s3_local_path, ext = ".xlsx")
    except FileNotFoundError:
        logger.error("Directory not found. Please provide a valid directory location to extract file names.")
        sys.exit(1)
    else:
        # read in file
        airport_path = s3_local_path + file_list[0]
        
        airport_df = load_file(path = airport_path, file_type = 'xlsx')

        f_origin = flag_international_airports(airport_df, **config['airport']['origin'])
        f_dest = flag_international_airports(airport_df, **config['airport']['dest'])


    # load processed data
    df = load_file(path = cleaned_path, file_type = 'csv')

    # convert variables to string
    df = convert_str(df, **config['convert_str'])

    # create subset to generate features from
    features_set = subset(df, **config['create_subset'])

    # generate features
    logger.info('Generating derived attributes')
    org_week_day = calculate_flight_averages(features_set, **config['features']['day_of_week'])
    org_dep_time = calculate_flight_averages(features_set, **config['features']['origin_time'])
    dest_arr_time = calculate_flight_averages(features_set, **config['features']['dest_time'])
    
    # merge features 
    logger.info('Merging generated features')
    df = merge_features(df, org_week_day, **config['merge']['day_of_week'])
    df = merge_features(df, org_dep_time, **config['merge']['origin_time'])
    df = merge_features(df, dest_arr_time, **config['merge']['dest_time'])
    df = merge_features(df, f_origin, **config['merge']['airport_origin'])
    df = merge_features(df, f_dest, **config['merge']['airport_dest'])

    # confirm expected columns
    expected_columns = ['FlightDate','Year','Month', 'DayofMonth', 'DayOfWeek','Reporting_Airline', 
                        'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime','ArrDelay', 'Cancelled', 'Diverted', 
                        'Flights', 'DepTime_blk', 'ArrTime_blk', 'Delay_group', 'DepTime_cat', 
                        'ArrTime_cat', 'avg_org_day_airline', 'avg_org_time_airline', 'avg_dest_time_airline', 
                        'f_int_origin', 'f_int_dest']
    included_columns = list(df.columns)
    if included_columns != expected_columns:
        logger.warning('After processing data, not all expected columns are included in this set.')
        missing = list(set(expected_columns) - set(included_columns))
        logger.debug('The following columns were expected but not included: {}'.format(missing))
    else:
        logger.info('The processed dataset includes the following columns: {}'.format(included_columns))
    
    # save out file 
    try:
        df.to_csv(processed_path, index = False)
        logger.info('Processed data was written to {}'.format(processed_path))
    except FileNotFoundError:
        logger.error('The path to save this file does not exist.')
        sys.exit(1)


