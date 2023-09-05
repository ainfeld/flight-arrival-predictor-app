import sys
import argparse
import logging

import pandas as pd
import yaml

from src.helpers import load_file

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger('clean_data')

def remove_observations(df, columns):
    """ Omit observations that are not included in scope for this analysis
    Args: 
        df (dataframe): pandas dataframe of full dataset
        columns (list): list of columns to flag observations to be removed
    Return:
        df (dataframe): dataframe with removed observations
    """
    # determine current number of observations
    current_size = len(df)
    if type(columns) != list:
        columns = [columns]
    for var in columns: 
        try: 
            df = df[df[var] != 1]
        except KeyError:
            logger.error('Column {} does not exist.'.format(var)) 
        else:
            new_size = len(df)
            diff = current_size - new_size
            logger.info('Removed {} {} flights.'.format(diff, var))

    logger.info('After removing cancelled and diverted flights, the dataset includes {} flights.'.format(len(df)))
    return df

def create_hour_block(df, old, new):
    """ Extracts hour from a time variable
    Args:
        df (dataframe): pandas dataframe of dataset
        old (list): list of time variables to extract hour from
        new (list): list of variable names to store hour values in
    Return: 
        df (dataframe): dataframe with additional hour columns
    """
    # check if length of list of original variables match the length of list of new variables
    if type(old) != list:
        old = [old]
    if type(new) != list:
        new = [new]
    for i in range(len(new)):
        if new[i] in list(df.columns):
            logger.warning('Column {} is about to be overwritten.'.format(new[i]))
        try:
            # attempt to extract hour
            df[old[i]] = df[old[i]].astype(str) 
        except IndexError:
            logger.error('Attempted to create more hour columns than time columns available.')
        except KeyError:
            logger.error('Column {} does not exist.'.format(old[i]))
        else:
            try:
                df[new[i]] = df[old[i]].str[:-2]
                df.loc[(df[new[i]] == "24"), new[i]] = '0'
                df.loc[(df[new[i]] == ""),new[i]] = '0'
                df[new[i]] = df[new[i]].astype(int)
            except KeyError:
                logger.error('Column {} does not exist.'.format(old[i]))
            except ValueError:
                logger.error('Column {} cannot be converted into an integer.'.format(new[i]))
            else:
                # confirm hours are between 0 and 24 
                hours = list(df[new[i]].unique())
                if not all(hour < 24 for hour in hours):
                    logger.warning('The hours are not within the 24 hour clock')
                    odd_hours = [hour for hour in hours if hour >= 24]
                    logger.debug('The following hour values are outside of the 24 hour clock: {}'.format(odd_hours))


    return df

def create_delay_category(df, old, new, values):
    """ Creates variable with delay category classifications
    Args:
        df (dataframe): pandas dataframe of dataset
        old (str): variable to base categorization on
        new (str): name of new category variable 
        values (list): list of delay category labels
    Return:
        df (dataframe): dataframe with additional delay categorization
    """
    if type(values) != list:
        values = [values]
    # check if column already exists
    if new in list(df.columns):
        logger.warning('Column {} is about to be overwritten.'.format(new))

    df[new] = None
    # check if the number of categories is correct
    if len(values) == 3:
        try:
            # assign categories to new variable based on each condition
            df.loc[(df[old] >= -30) & (df[old] <= 30), new] = values[1]
            df.loc[(df[old] < -30), new] = values[0]
            df.loc[(df[old] > 30), new] = values[2]
        except KeyError:
            logger.error('Column {} does not exist.'.format(old))
        except TypeError:
            logger.error('Incorrect column: {} - cannot create category off of non-integer variable'.format(old))
    else: 
        logger.error('Incorrect length of values.')

    return df

def create_time_category(df, old, new, values):
    """ Creates variable with time categorization (Morning, Afternon/Evening, and Night)
    Args:
        df (dataframe): pandas dataframe of dataset
        old (list): list of hour variables to create categorization from
        new (list): list of variable names to store hour categorization in
        values (list): list of time category labels
    Return:
        df (dataframe): dataframe with additional time categorizations
    """
    lists = [old, new, values]
    for list_name in lists:
        if type(list_name) != list:
            list_name = [list_name]
    if len(values) == 3:
        for i in range(len(new)):
            # check if column already exists 
            if new[i] in list(df.columns):
                logger.warning('Column {} is about to be overwritten.'.format(new[i]))
            df[new[i]] = None
            try:
                # assign categories to new variable based on each condition
                df.loc[(df[old[i]] >= 5) & (df[old[i]] <= 11), new[i]] = values[0]
                df.loc[(df[old[i]] >= 12) & (df[old[i]] <= 19), new[i]] = values[1]
                df.loc[(df[old[i]] <= 4) | (df[old[i]] >= 20), new[i]] = values[2]
            except IndexError:
                logger.error('Attempted to create more time category columns than time columns available.')
            except KeyError:
                logger.error('Column {} does not exist.'.format(old[i]))
            except TypeError:
                logger.error('Incorrect column: {} - cannot create category off of non-integer variable'.format(old[i]))
    else:
        logger.error('Incorrect length of values.')

    return df

def run_clean_data(config_path, raw_path, cleaned_path):
    """ Run clean data script 
    Args:
        config_path (str): path to yaml configuration file
        raw_path (str): path to file raw version of the data was stored
        cleaned_path (str): path to file cleaned version of the data should be stored 
    Returns:
        None
    """
    # load yaml configuration file
    try:
        with open(config_path, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            config = config['clean_data']
    except FileNotFoundError:
        logger.error('The following file was not found: {} \n Please provide a valid path to the configuration file.'.format(config_path))
        sys.exit(1)

    # load raw data
    df = load_file(path = raw_path, file_type = 'csv')

    # remove flights that were cancelled or diverted from the analysis set
    df = remove_observations(df, **config['remove_observations'])

    # extract hour from time variables
    logger.info('Creating hour blocks')
    df = create_hour_block(df, **config['hour_block'])
    
    # label flights as on-time, early, or late based on their delay time
    logger.info('Creating delay category')
    df = create_delay_category(df, **config['delay_category'])

    # classify flights by time of day
    logger.info('Creating time category')
    df = create_time_category(df, **config['time_category'])

    expected_columns = ['FlightDate','Year','Month', 'DayofMonth', 'DayOfWeek','Reporting_Airline', 
                        'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime','ArrDelay', 'Cancelled', 'Diverted', 
                        'Flights', 'DepTime_blk', 'ArrTime_blk', 'Delay_group', 'DepTime_cat', 'ArrTime_cat']
    included_columns = list(df.columns)
    if included_columns != expected_columns:
        logger.warning('After cleaning up data, not all expected columns are included in this set.')
        missing = list(set(expected_columns) - set(included_columns))
        logger.debug('The following columns were expected but not included: {}'.format(missing))
    else:
        logger.info('The cleaned dataset includes the following columns: {}'.format(included_columns))

    try:
        df.to_csv(cleaned_path, index = False)
        logger.info('Cleaned data was written to {}'.format(cleaned_path))
    except FileNotFoundError:
        logger.error('The path to save this file does not exist.')
        sys.exit(1)

    

