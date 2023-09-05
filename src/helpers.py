from os import path
import glob
import sys

import logging
import pandas as pd


logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger('helpers')

def get_file_names(dir_path, ext):
    """Get all file names in a directory subtree
    Args: 
        dir_path (str): The base directory from which to get list_of_files from
    Returns: 
        file_names (str): List of file names
    """

    isdir = path.isdir(dir_path)

    if not isdir: 
        raise FileNotFoundError

    file_names = [path.basename(x) for x in glob.glob(dir_path+'*'+ext)]

    return file_names

def load_file(path, file_type):
    """ load file of data into a pandas dataframe 
    Args:
        path (str): path of data file to load 
        file_type (str): whether uploading csv or xlsx file (options: 'csv', 'xlsx')
    Returns:
        df (dataframe): dataframe created from data file
    """
    # read in csv to dataframe
    if file_type in ['csv', 'xlsx']:
        try:    
            logger.debug('Reading in {}'.format(path))
            if file_type == 'csv':
                df = pd.read_csv(path)
            elif file_type == 'xlsx':
                df = pd.read_excel(path)
            logger.debug('Successfully read in {}'.format(path))
            return df
        except FileNotFoundError:
            logger.error('The following file was not found {}. Please provide a valid file path'.format(path))
            sys.exit(1)
    else: 
        logger.error('Not a valid file type option.')
        sys.exit(1)

def subset(df, columns):
    """ Create subset of dataset
    Args:
        df (dataframe): pandas dataframe of dataset
        columns (list): list of columns to include in the subset
    Returns:
        df (dataframe): subset of original dataframe with requested columns
    """
    try: # subset dataframe to specified columns
        df = df[columns]
    except KeyError:
        logger.error('One or more columns do not exist: {}'.format(columns))

    return df



