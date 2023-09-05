import os
import glob
import argparse
import logging

import sys
import boto3
import yaml


logging.getLogger("s3transfer").setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logger = logging.getLogger('acquire_data')

def get_s3_file_names(aws_access_key_id, aws_secret_access_key, Bucket, s3_bucket_path):
    """ Compile list of file names from a specific location in S3
    Args:
        aws_access_key_id (str): AWS access key id credential
        aws_secret_access_key (str): AWS secret access key credential
        Bucket (str): name of AWS bucket to pull data from
        s3_bucket_path (str): path in S3 where raw data is stored
    Returns:
        file_list (list): list of file names
    """
    file_list = []
    # connect to s3 bucket
    try:
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        s3_list = s3.list_objects(Bucket = Bucket, Prefix=s3_bucket_path)['Contents']
    except FileNotFoundError:
        logger.error("The location in S3 to download data from does not exist: {}".format(s3_bucket_path))
        sys.exit(1)
    except:
        logger.error("An error occurred, please try again.")
        sys.exit(1)
    else:
        # store list of files to download
        for file in s3_list:
            file_name = file['Key']
            file_list.append(file_name)
        logger.info("There were {} file names retrieved.".format(len(file_list)))
        return file_list

def download_from_s3(aws_access_key_id, aws_secret_access_key, s3_path, local_path, Bucket):
    """ Download file from S3 bucket to local environment
    Args:
        aws_access_key_id (str): AWS access key id credential
        aws_secret_access_key (str): AWS secret access key credential
        s3_path (str): path of file in S3 bucket to download 
        local_path (str): path of file to save on local computer
        Bucket (str): name of AWS bucket to pull data from
    Return: 
        boolean of whether the file downloaded was successful or not
    """
    try:
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        s3.download_file(Bucket, s3_path, local_path)
        logger.info("Successful download of file {}".format(local_path))
        return True
    except FileNotFoundError:
        logger.error("The location to save this file does not exist: {}".format(local_path))
        return False
    except:
        logger.error("An error occurred, please try again.")
        return False

def download_set(aws_access_key_id, aws_secret_access_key, Bucket, s3_bucket_path, s3_local_path, file_list, ext, ith_file):
    """ Download set of files from S3
    Args:
        aws_access_key_id (str): AWS access key id credential
        aws_secret_access_key (str): AWS secret access key credential
        Bucket (str): name of AWS bucket to pull data from
        s3_bucket_path (str): path in S3 where raw data is stored
        s3_local_path (str): path on local where raw data from S3 should be stored
        file_list (list): list of file names to download
        ext (string): extension of files to download
        ith_file (int): ith number of file to pull to create subset
    Returns:
        count (int): number of files successfully downloaded
    """
    # Count the number of files successfully downloaded
    count = 0
    file_num = 0

    # Download data from S3
    for file in file_list:
        file_name = file.replace(s3_bucket_path, '')
        file_num += 1
        if (ext in file_name) & (file_num%ith_file==0):
            local_path = s3_local_path + file_name
            if (os.path.isfile(local_path))==True:
                logger.warning('The file {} already exists and will be overwritten.'.format(local_path))
            value = download_from_s3(aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key, 
                                     s3_path = file, local_path = local_path, Bucket = Bucket)
            count +=1*value
    return count

def s3_to_local(config_path, aws_access_key_id, aws_secret_access_key, Bucket, s3_bucket_path, s3_local_path):
    """ Download all files from a location in the S3 bucket to local environment
    Args: 
        config_path (str): path to yaml configuration file
        aws_access_key_id (str): AWS access key id credential
        aws_secret_access_key (str): AWS secret access key credential
        Bucket (str): name of AWS bucket to pull data from
        s3_bucket_path (str): path in S3 where raw data is stored
        s3_local_path (str): path on local where raw data from S3 should be stored
    Return: 
        None
    """
    # load yaml configuration file
    try:
        with open(config_path, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            config = config['acquire_data']
    except FileNotFoundError:
        logger.error('The following file was not found: {} \n Please provide a valid path to the configuration file.'.format(config_path))
        sys.exit(1)

    # retrieve file names in S3 bucket
    file_list = get_s3_file_names(aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key, 
                                  Bucket = Bucket, s3_bucket_path = s3_bucket_path)

    # download delay data subset 
    count_delay = download_set(aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key, Bucket = Bucket, 
                 s3_bucket_path = s3_bucket_path, s3_local_path = s3_local_path, file_list = file_list, **config['delay_data'])

    # download international airport data
    count_airport = download_set(aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key, Bucket = Bucket, 
                 s3_bucket_path = s3_bucket_path, s3_local_path = s3_local_path, file_list = file_list, **config['airport_data'])

    total = count_delay + count_airport
    logger.info("You have successfully downloaded {} files from the S3 bucket.".format(total))
        
    


    

    
