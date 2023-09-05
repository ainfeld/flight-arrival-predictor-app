import argparse
import logging.config
import csv
import random
import numpy as np
import sys

import pandas as pd
import yaml
import pickle

# for modeling
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

from src.helpers import load_file

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger('modeling')

def convert_categorical(df, columns):
    """ convert columns to categorical variables 
    Args:
        df (dataframe): dataframe of full dataset
        columns (list): list of columns to convert to categorical
    Returns:
        df (dataframe): dataframe with columns converted to categorical
    """
    for col in columns:
        try:
            df[col] = df[col].astype('category')
            df[col] = df[col].cat.codes
        except KeyError:
            logger.error('Column {} does not exist.'.format(col))

    return df

def create_train_test(df, column, date, features, target):
    """ create_train_test
    Args: 
        df (dataframe): dataframe of full dataset
        column (str): name of variable to filter sets
        date (str): date to separate test and train sets
        features (list): columns that make up input set
        target (str): name of column to use as the output the model is trying to predict
    Returns:
        train_X (dataframe): input set to train the model on 
        test_X (dataframe): input set to test the trained model on
        train_Y (series): series of output values used to train the model
        test_Y (series): series of output values used to test the trained model
    """
    # confirm type list
    if type(features) != list:
        features = [features]
    if type(target) != list:
        target = [target]

    try: # create test and train sets
        train = df[df[column] < date]
        test = df[df[column] >= date]
    except KeyError:
        logger.error('Column {} does not exist.'.format(column))

    try: # create input sets
        train_X = train[features]
        test_X = test[features]
    except KeyError:
        logger.error('Attempted to create input sets, but one or more columns do not exist: {}'.format(features))
    except NameError:
        logger.error('One or both of the dataframes does not exist: train, test')
    else:
        try: # create output sets
            train_Y = train[target].values.ravel()
            test_Y = test[target].values.ravel()
        except KeyError:
            logger.error('Column {} does not exist.'.format(target))
        except NameError:
            logger.error('One or both of the dataframes does not exist: train, test')
        else:
            return train_X, test_X, train_Y, test_Y

def train_model(train_X, train_Y, n_estimators, max_depth, max_features, random_state, n_jobs):
    """ train model based on parameters determine through testing
    Args:
        train_X (dataframe): input set to train the model on 
        train_Y (series): series of output values used to train the model
        n_estimators (int): number of trees in the forest
        max_depth (int): maximum depth of the tree
        max_features (int): the number of features to consider when looking for the best split
        random_state (int): randomly generated number used to make the model repoducible 
        n_jobs (int): number of jobs to run in parallel, -1 means use all processors
    Returns:
        model (sklearn model): trained random forest classifier model 
    """
    try: # fit model
        model = RandomForestClassifier(n_estimators = n_estimators, max_depth=max_depth, 
                                       max_features = max_features, random_state = random_state, 
                                       n_jobs = n_jobs)
        model.fit(train_X, train_Y)
        return model
    except ValueError:
        logger.error('Invalid model parameter.')
    except:
        logger.error('An error has occurred')

def make_prediction(model, set_X):
    """ Make predictions on new observations using fitted model
    Args:
        model (sklearn model): trained random forest classifier model 
        set_X (dataframe): input set to make predictions on 
    Returns:
        predictions (series): predictions on input set using fitted model
    """
    try:
        predictions = model.predict(set_X)
        return predictions
    except ValueError:
        logger.error('Test set does not match the format of the trained model.')
    except AttributeError:
        logger.error('Model object does not exist')
    except:
        logger.error('An error has occurred')

def score_model(predictions, test_Y, average): 
    """ Make predictions on test set and score the model
    Args:
        predidtions (series): predictions on test set using fitted model
        test_Y (series): series of output values used to test the trained model
        average (str): type of averaging performed on the data
    Returns:
        string (str): string reporting model performance metric
    """
    try: # score model
        score = f1_score(test_Y, predictions, average = average)
    except ValueError:
        if len(test_Y) != len(predictions):
            logger.error('The prediction set and test set are not the same length.')
        elif average not in [None, 'binary', 'micro', 'macro', 'samples', 'weighted']:
            logger.error('{} is not an option. Average has to be one of (None, micro, macro, weighted, samples)'.format(average))  
        else:
            logger.error('An error has occured')
    else:
        string = 'F1-score: ' + str(score) 
        logger.info(string)
        return string

def run_modeling(config_path, processed_path, metrics_path, predictions_path, model_path):
    """ Run modeling script
    Args:
        config_path (str): path to yaml configuration file
        processed_path (str): path of file with the processed version of the data
        metrics_path (str): path of file metrics should be stored in
        predictions_path (str): path of file predictions should be stored in 
        model_path (str): path of file model object should be stored
    Returns:
        None
    """
    try:
        with open(config_path, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            config = config['modeling']
    except FileNotFoundError:
        logger.error('The following file was not found: {} \n Please provide a valid path to the configuration file.'.format(config_path))
        sys.exit(1)

    # load processed data
    df = load_file(path = processed_path, file_type = 'csv')

    # convert columns to categorical
    df = convert_categorical(df, **config['convert_categorical'])

    # create train and test sets
    logger.info('Creating train and test sets')
    train_X, test_X, train_Y, test_Y = create_train_test(df, **config['create_train_test'])

    # train model
    logger.info('Training the model')
    model = train_model(train_X = train_X, train_Y = train_Y, **config['train_model'])

    try:
        parameters = model.get_params()
        logger.info('Parameters: {}'.format(parameters))
    except TypeError:
        logger.error('Trained model does not exist.')

    # make predictions on test set 
    logger.info('Making predictions')
    predictions = make_prediction(model = model, set_X = test_X)

    # save out predictions results
    if predictions is not None:
        df_test_X = test_X.reset_index(drop=True)
        pred_df = pd.DataFrame(predictions, columns = ['Predictions'])
        actual_df = pd.DataFrame(test_Y, columns = ['Actual'])
        prediction_results = pd.concat([df_test_X, actual_df], axis = 1)
        prediction_results = pd.concat([prediction_results, pred_df], axis = 1)
        try:
            prediction_results.to_csv(predictions_path)
            logger.debug('Prediction results were saved to {}.'.format(predictions_path))
        except FileNotFoundError:
            logger.error('The path to save the prediction results does not exist.')
            sys.exit(1)

    # score_model
    logger.info('Scoring the model')
    performance_metric = score_model(predictions = predictions, test_Y = test_Y, **config['score_model'])

    try: # save out files
        with open(metrics_path, 'w') as f:
            print(performance_metric, file = f)
        logger.debug('Model result was written to {}.'.format(metrics_path))
    except FileNotFoundError:
        logger.error('The following file was not found {}.'.format(metrics_path))

    # build model for app
    input_set = pd.concat([train_X, test_X]) 
    output_set = np.append(train_Y,test_Y)

    app_model = train_model(train_X = input_set, train_Y = output_set, **config['train_model'])

    try:
        pickle.dump(model, open(model_path, 'wb'))
        logger.debug('Model object was saved to {}.'.format(model_path))
    except FileNotFoundError:
        logger.error('The path to save the trained model does not exist.')
        sys.exit(1)
