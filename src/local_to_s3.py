import os
import glob
import argparse
import sys

import config
import logging.config

import yaml
import boto3

from src.helpers import get_file_names

logging.getLogger("s3transfer").setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logger = logging.getLogger('local_to_s3')


def upload_to_s3(aws_access_key_id, aws_secret_access_key, Bucket, local_path, s3_path):
    """ Upload file from local environment to S3 bucket
    Args: 
        aws_access_key_id (str): AWS access key id credential
        aws_secret_access_key (str): AWS secret access key credential
        Bucket (str): name of AWS bucket to upload data to
        local_path (str): path of file on local computer to upload 
        s3_path (str): path of file to save in S3 bucket
    Return: 
        boolean of whether the file upload was successful or not
    """
    try:
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        s3.upload_file(local_path, Bucket, s3_path)
        logger.info("Successful upload of file {}".format(s3_path))
        return True
    except FileNotFoundError:
        logger.error("The following file was not found: {}".format(local_path))
        return False
    except:
        logger.error("An error occurred, please try again.")
        return False

def upload_set(aws_access_key_id, aws_secret_access_key, Bucket, raw_local_path, s3_bucket_path, file_list):
    """ Upload all files from a location in your local environment to s3
    Args: 
        aws_access_key_id (str): AWS access key id credential
        aws_secret_access_key (str): AWS secret access key credential
        Bucket (str): name of AWS bucket to upload data to
        raw_local_path (str): path on local where raw data is stored
        s3_bucket_path (str): path in S3 where raw data should be uploaded to
        file_list (list): list of file names to download
        ext (string): extension of files to download
    Return: 
        count (int): number of files successfully downloaded
    """
    # Count the number of files successfully uploaded
    count = 0

    # Upload data to S3
    for file in file_list: 
        local_path =  raw_local_path + file
        s3_path = s3_bucket_path + file
        value = upload_to_s3(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, Bucket = Bucket, local_path = local_path, s3_path = s3_path)
        count += 1*value

    return count

def local_to_s3(config_path, aws_access_key_id, aws_secret_access_key, Bucket, raw_local_path, s3_bucket_path):
    """ Upload all files from local environment to a location in the S3 bucket
    Args:
        config_path (str): path to yaml configuration file
        aws_access_key_id (str): AWS access key id credential
        aws_secret_access_key (str): AWS secret access key credential
        Bucket (str): name of AWS bucket to pull data from
        raw_local_path (str): path on local where raw data is stored
        s3_bucket_path (str): path in S3 where raw data should be uploaded to
    Returns:
        None
    """
    # load yaml configuration file
    try:
        with open(config_path, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            config = config['local_to_s3']
    except FileNotFoundError:
        logger.error('The following file was not found: {} \n Please provide a valid path to the configuration file.'.format(config_path))
        sys.exit(1)


    # Get list of filenames of files to upload to s3
    try:
        file_list = get_file_names(dir_path = raw_local_path, ext = '')
    except FileNotFoundError: 
        logger.error("Directory not found. Please provide a valid directory location to extract file names.")
        sys.exit(1)

    logger.info("There were {} file names retrieved.".format(len(file_list)))

    # Upload data to s3
    count = upload_set(aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key, Bucket = Bucket,
                       raw_local_path = raw_local_path, s3_bucket_path = s3_bucket_path, file_list = file_list)

    logger.info("You have successfully uploaded {} files to the S3 bucket.".format(count))

    

    
