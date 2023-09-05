import argparse
import logging
import config.flaskconfig as flask

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger('run-reproducibility')

from src.local_to_s3 import local_to_s3
from src.acquire_data import s3_to_local
from src.load_data import run_load_data
from src.clean_data import run_clean_data
from src.generate_features import run_generate_features
from src.modeling import run_modeling
from src.add_flights import set_up_db
from src.acquire_data import download_from_s3

from src.test_helpers import run_helper_tests
from src.test_load_data import run_load_data_tests
from src.test_clean_data import run_clean_data_tests
from src.test_generate_features import run_generate_features_tests
from src.test_modeling import run_modeling_tests
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run pipeline")

    parser.add_argument('option', help = 'Which script to run', choices = ['local_to_s3', 'acquire', 'load', 'clean', 'features', 'modeling', 
                                                                           'create_db', 'download_model', 'download_processed', 'helper_tests', 
                                                                           'load_data_tests', 'clean_data_tests', 'generate_features_tests', 
                                                                           'modeling_tests'])
    parser.add_argument('--config', help = 'Path to configuration file')
    parser.add_argument('--input_path', help = 'Path to input file')
    parser.add_argument('--output_path', help = 'Path to output')
    parser.add_argument('--dir_path', help = 'Path to data folder')
    parser.add_argument('--model_path', help = 'Path to save model')
    parser.add_argument('--predictions_path', help = 'Path to predictions')

    args = parser.parse_args()
    
    # Uploading data to S3
    if args.option == 'local_to_s3':
        local_to_s3(config_path = args.config, aws_access_key_id = flask.AWS_ACCESS_KEY_ID, aws_secret_access_key = flask.AWS_SECRET_ACCESS_KEY, 
                    Bucket = flask.AWS_BUCKET, raw_local_path = args.input_path , s3_bucket_path = args.output_path)

    # Running the model pipeline
    if args.option == 'acquire':
        s3_to_local(config_path = args.config, aws_access_key_id = flask.AWS_ACCESS_KEY_ID, aws_secret_access_key = flask.AWS_SECRET_ACCESS_KEY, 
                    Bucket = flask.AWS_BUCKET, s3_bucket_path = args.input_path , s3_local_path = args.output_path)
    if args.option == 'load':
        run_load_data(config_path = args.config, s3_local_path = args.input_path, raw_path = args.output_path)
    if args.option == 'clean':
        run_clean_data(config_path = args.config, raw_path = args.input_path, cleaned_path = args.output_path)
    if args.option == 'features':
        run_generate_features(config_path = args.config, cleaned_path = args.input_path, s3_local_path = args.dir_path, processed_path = args.output_path)
    if args.option == 'modeling':
        run_modeling(config_path = args.config, processed_path = args.input_path, metrics_path = args.output_path, model_path = args.model_path, predictions_path = args.predictions_path)

    # Creating the database
    if args.option == 'create_db':
        set_up_db(config_path = args.config, processed_path = args.input_path, engine_string = flask.SQLALCHEMY_DATABASE_URI)
    if args.option == 'download_model':
        download_from_s3(aws_access_key_id = flask.AWS_ACCESS_KEY_ID, aws_secret_access_key = flask.AWS_SECRET_ACCESS_KEY, 
                         s3_path = args.input_path, local_path = flask.APP_MODEL, Bucket = flask.AWS_BUCKET)
    if args.option == 'download_processed':
        download_from_s3(aws_access_key_id = flask.AWS_ACCESS_KEY_ID, aws_secret_access_key = flask.AWS_SECRET_ACCESS_KEY, 
                         s3_path = args.input_path, local_path = args.output_path, Bucket = flask.AWS_BUCKET)

    # Running tests
    if args.option == 'helper_tests':
        run_helper_tests()
    if args.option == 'load_data_tests':
        run_load_data_tests()
    if args.option == 'clean_data_tests':
        run_clean_data_tests()
    if args.option == 'generate_features_tests':
        run_generate_features_tests()
    if args.option == 'modeling_tests':
        run_modeling_tests()



