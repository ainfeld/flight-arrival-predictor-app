import src.modeling as md
import pandas as pd
import logging
import sklearn

logger = logging.getLogger('test_modeling')

def create_train_test_happy():
    inputs = [['2018-01-11', 2018, 1, 11, 4, 2, 7, 20, 735, 1004, 10.0, 0.0,
                0.0, 1.0, 7, 10, 2, 'Morning', 'Morning', 696.6666666666665,
                199.7041095890411, 10.222120658135283, 1.0, 1.0],
               ['2018-01-11', 2018, 1, 11, 4, 2, 7, 20, 850, 1121, -9.0, 0.0,
                0.0, 1.0, 8, 11, 2, 'Morning', 'Morning', 696.6666666666665,
                199.7041095890411, 10.222120658135283, 1.0, 1.0],
               ['2017-10-26', 2017, 10, 26, 4, 2, 7, 20, 736, 1010, -6.0, 0.0,
                0.0, 1.0, 7, 10, 2, 'Morning', 'Morning', 696.6666666666665,
                199.7041095890411, 10.222120658135283, 1.0, 1.0],
               ['2017-10-26', 2017, 10, 26, 4, 2, 7, 20, 855, 1125, -6.0, 0.0,
                0.0, 1.0, 8, 11, 2, 'Morning', 'Morning', 696.6666666666665,
                199.7041095890411, 10.222120658135283, 1.0, 1.0],
               ['2017-10-05', 2017, 10, 5, 4, 2, 7, 20, 736, 1010, -4.0, 0.0,
                0.0, 1.0, 7, 10, 2, 'Morning', 'Morning', 696.6666666666665,
                199.7041095890411, 10.222120658135283, 1.0, 1.0],
               ['2019-06-14', 2019, 6, 14, 5, 3, 110, 84, 640, 816, 10.0, 0.0,
                0.0, 1.0, 6, 8, 2, 'Morning', 'Morning', 2.333333333333333,
                1.534957627118644, 57.751831501831504, 1.0, 1.0],
               ['2019-06-21', 2019, 6, 21, 5, 3, 110, 84, 640, 816, -17.0, 0.0,
                0.0, 1.0, 6, 8, 2, 'Morning', 'Morning', 2.333333333333333,
                1.534957627118644, 57.751831501831504, 1.0, 1.0],
               ['2019-06-07', 2019, 6, 7, 5, 3, 110, 84, 640, 816, -8.0, 0.0,
                0.0, 1.0, 6, 8, 2, 'Morning', 'Morning', 2.333333333333333,
                1.534957627118644, 57.751831501831504, 1.0, 1.0],
               ['2017-09-15', 2017, 9, 15, 5, 3, 110, 84, 622, 807, 8.0, 0.0,
                0.0, 1.0, 6, 8, 2, 'Morning', 'Morning', 2.333333333333333,
                1.534957627118644, 57.751831501831504, 1.0, 1.0],
               ['2017-09-29', 2017, 9, 29, 5, 3, 110, 84, 622, 807, -26.0, 0.0,
                0.0, 1.0, 6, 8, 2, 'Morning', 'Morning', 2.333333333333333,
                1.534957627118644, 57.751831501831504, 1.0, 1.0]]

    input_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                  'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 
                  'CRSArrTime', 'ArrDelay', 'Cancelled', 'Diverted', 'Flights', 
                  'DepTime_blk', 'ArrTime_blk', 'Delay_group', 'DepTime_cat', 
                  'ArrTime_cat', 'avg_org_day_airline', 'avg_org_time_airline', 
                  'avg_dest_time_airline', 'f_int_origin', 'f_int_dest']

    df_input = pd.DataFrame(inputs, columns = input_cols)

    actual_X_cols = ['Month', 'DayofMonth', 'DayOfWeek', 'Reporting_Airline', 
                     'Origin', 'Dest', 'DepTime_blk', 'ArrTime_blk', 'avg_org_day_airline', 
                     'avg_org_time_airline', 'avg_dest_time_airline', 'f_int_origin', 'f_int_dest']

    actual_trainX = [[  1        ,  11        ,   4        ,   2        ,
                          7        ,  20        ,   7        ,  10        ,
                        696.66666667, 199.70410959,  10.22212066,   1.0        ,
                          1.0        ],
                       [  1        ,  11        ,   4        ,   2        ,
                          7        ,  20        ,   8        ,  11        ,
                        696.66666667, 199.70410959,  10.22212066,   1.0        ,
                          1.0        ],
                       [ 10        ,  26        ,   4        ,   2        ,
                          7        ,  20        ,   7        ,  10        ,
                        696.66666667, 199.70410959,  10.22212066,   1.0        ,
                          1.0        ],
                       [ 10        ,  26        ,   4        ,   2        ,
                          7        ,  20        ,   8        ,  11        ,
                        696.66666667, 199.70410959,  10.22212066,   1.0        ,
                          1.0        ],
                       [ 10        ,   5        ,   4        ,   2        ,
                          7        ,  20        ,   7        ,  10        ,
                        696.66666667, 199.70410959,  10.22212066,   1.0        ,
                          1.0        ],
                       [  9        ,  15        ,   5        ,   3        ,
                        110        ,  84        ,   6        ,   8        ,
                          2.33333333,   1.53495763,  57.7518315 ,   1.0        ,
                          1.0        ],
                       [  9        ,  29        ,   5        ,   3        ,
                        110        ,  84        ,   6        ,   8        ,
                          2.33333333,   1.53495763,  57.7518315 ,   1.0        ,
                          1.0        ]]

    df_actual_trainX = pd.DataFrame(actual_trainX, columns = actual_X_cols)

    actual_testX = [[  6        ,  14        ,   5        ,   3        ,
                        110        ,  84        ,   6        ,   8        ,
                          2.33333333,   1.53495763,  57.7518315 ,   1        ,
                          1        ],
                       [  6        ,  21        ,   5        ,   3        ,
                        110        ,  84        ,   6        ,   8        ,
                          2.33333333,   1.53495763,  57.7518315 ,   1.0        ,
                          1.0        ],
                       [  6        ,   7        ,   5        ,   3        ,
                        110        ,  84        ,   6        ,   8        ,
                          2.33333333,   1.53495763,  57.7518315 ,   1.0        ,
                          1.0        ]]

    df_actual_testX = pd.DataFrame(actual_testX, columns = actual_X_cols)

    actual_trainY = [2, 2, 2, 2, 2, 2, 2]

    actual_testY = [2, 2, 2]

    column = 'FlightDate'
    date = '2019-04-01'
    features = ['Month', 'DayofMonth','DayOfWeek','Reporting_Airline', 
                   'Origin', 'Dest', 'DepTime_blk', 'ArrTime_blk', 'avg_org_day_airline', 
                   'avg_org_time_airline', 'avg_dest_time_airline', 'f_int_origin', 'f_int_dest']
    target = ['Delay_group']

    df_train_X, df_test_X, train_Y, test_Y = md.create_train_test(df_input, column, date, features, target)

    df_train_X = df_train_X.reset_index(drop=True).round(4)
    df_test_X = df_test_X.reset_index(drop=True).round(4)

    df_actual_trainX = df_actual_trainX.round(4)
    df_actual_testX = df_actual_testX.round(4)

    assert df_train_X.equals(df_actual_trainX)
    assert df_test_X.equals(df_actual_testX)
    assert all(actual_trainY == train_Y) == True
    assert all(actual_testY == test_Y) == True

def create_train_test_unhappy():

    inputs = [['2018-01-11', 2018, 1, 11, 4, 2, 7, 20, 735, 1004, 10.0, 0.0,
                0.0, 1.0, 7, 10, 2, 'Morning', 'Morning', 696.6666666666665,
                199.7041095890411, 10.222120658135283, 1.0, 1.0],
               ['2018-01-11', 2018, 1, 11, 4, 2, 7, 20, 850, 1121, -9.0, 0.0,
                0.0, 1.0, 8, 11, 2, 'Morning', 'Morning', 696.6666666666665,
                199.7041095890411, 10.222120658135283, 1.0, 1.0],
               ['2017-10-26', 2017, 10, 26, 4, 2, 7, 20, 736, 1010, -6.0, 0.0,
                0.0, 1.0, 7, 10, 2, 'Morning', 'Morning', 696.6666666666665,
                199.7041095890411, 10.222120658135283, 1.0, 1.0],
               ['2017-10-26', 2017, 10, 26, 4, 2, 7, 20, 855, 1125, -6.0, 0.0,
                0.0, 1.0, 8, 11, 2, 'Morning', 'Morning', 696.6666666666665,
                199.7041095890411, 10.222120658135283, 1.0, 1.0],
               ['2017-10-05', 2017, 10, 5, 4, 2, 7, 20, 736, 1010, -4.0, 0.0,
                0.0, 1.0, 7, 10, 2, 'Morning', 'Morning', 696.6666666666665,
                199.7041095890411, 10.222120658135283, 1.0, 1.0]]

    input_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                  'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 
                  'CRSArrTime', 'ArrDelay', 'Cancelled', 'Diverted', 'Flights', 
                  'DepTime_blk', 'ArrTime_blk', 'Delay_group', 'DepTime_cat', 
                  'ArrTime_cat', 'avg_org_day_airline', 'avg_org_time_airline', 
                  'avg_dest_time_airline', 'f_int_origin', 'f_int_dest']

    df_input = pd.DataFrame(inputs, columns = input_cols)

    actual_X_cols = ['Month', 'DayofMonth', 'DayOfWeek', 'Reporting_Airline', 
                     'Origin', 'Dest', 'DepTime_blk', 'ArrTime_blk', 'avg_org_day_airline', 
                     'avg_org_time_airline', 'avg_dest_time_airline', 'f_int_origin', 'f_int_dest']

    actual_trainX = [[  1        ,  11        ,   4        ,   2        ,
                        7        ,  20        ,   7        ,  10        ,
                      696.66666667, 199.70410959,  10.22212066,   1.0        ,
                        1.0        ],
                     [  1        ,  11        ,   4        ,   2        ,
                        7        ,  20        ,   8        ,  11        ,
                      696.66666667, 199.70410959,  10.22212066,   1.0        ,
                        1.0        ],
                     [ 10        ,  26        ,   4        ,   2        ,
                        7        ,  20        ,   7        ,  10        ,
                      696.66666667, 199.70410959,  10.22212066,   1.0        ,
                        1.0        ],
                     [ 10        ,  26        ,   4        ,   2        ,
                        7        ,  20        ,   8        ,  11        ,
                      696.66666667, 199.70410959,  10.22212066,   1.0        ,
                        1.0        ],
                     [ 10        ,   5        ,   4        ,   2        ,
                        7        ,  20        ,   7        ,  10        ,
                      696.66666667, 199.70410959,  10.22212066,   1.0        ,
                        1.0        ]]

    df_actual_trainX = pd.DataFrame(actual_trainX, columns = actual_X_cols)

    actual_testX = []

    df_actual_testX = pd.DataFrame(actual_testX, columns = actual_X_cols)

    actual_trainY = [2, 2, 2, 2, 2]

    actual_testY = []

    column = 'FlightDate'
    date = '2019-04-01'
    features = ['Month', 'DayofMonth','DayOfWeek','Reporting_Airline', 
                   'Origin', 'Dest', 'DepTime_blk', 'ArrTime_blk', 'avg_org_day_airline', 
                   'avg_org_time_airline', 'avg_dest_time_airline', 'f_int_origin', 'f_int_dest']
    target = ['Delay_group']

    df_train_X, df_test_X, train_Y, test_Y = md.create_train_test(df_input, column, date, features, target)

    df_train_X = df_train_X.reset_index(drop=True).round(4)

    df_actual_trainX = df_actual_trainX.round(4)

    assert df_train_X.equals(df_actual_trainX)
    assert df_test_X.empty & df_actual_testX.empty

    assert all(actual_trainY == train_Y) == True
    assert all(actual_testY == test_Y) == True

def test_make_prediction_happy():
    train_X = [[ 1.        ,  1.        ,  7.        ,  0.        , 92.        ,
                96.        ,  8.        , 11.        , 46.26785714, 17.03523035,
                32.06775068,  1.        ,  1.        ],
               [ 1.        ,  8.        ,  7.        ,  0.        , 92.        ,
                96.        ,  8.        , 11.        , 46.26785714, 17.03523035,
                32.06775068,  1.        ,  1.        ],
               [ 1.        , 22.        ,  7.        ,  0.        , 92.        ,
                96.        ,  8.        , 11.        , 46.26785714, 17.03523035,
                32.06775068,  1.        ,  1.        ],
               [ 1.        , 29.        ,  7.        ,  0.        , 92.        ,
                96.        ,  8.        , 11.        , 46.26785714, 17.03523035,
                32.06775068,  1.        ,  1.        ],
               [ 1.        ,  1.        ,  7.        ,  0.        , 92.        ,
                96.        ,  7.        , 10.        , 46.26785714, 17.03523035,
                32.06775068,  1.        ,  1.        ],
               [ 1.        ,  8.        ,  7.        ,  0.        , 92.        ,
                96.        ,  7.        , 10.        , 46.26785714, 17.03523035,
                32.06775068,  1.        ,  1.        ],
               [ 1.        , 29.        ,  7.        ,  0.        , 92.        ,
                96.        ,  7.        , 10.        , 46.26785714, 17.03523035,
                32.06775068,  1.        ,  1.        ],
               [12.        , 23.        ,  7.        ,  0.        , 92.        ,
                96.        ,  8.        , 11.        , 46.26785714, 17.03523035,
                32.06775068,  1.        ,  1.        ]]

    input_X_cols = ['Month', 'DayofMonth', 'DayOfWeek', 'Reporting_Airline', 'Origin', 'Dest', 'DepTime_blk', 
                    'ArrTime_blk', 'avg_org_day_airline', 'avg_org_time_airline', 'avg_dest_time_airline', 
                    'f_int_origin', 'f_int_dest']  

    df_train_X = pd.DataFrame(train_X, columns = input_X_cols)

    train_Y = [2, 2, 1, 0, 1, 1, 0, 0]

    actual_parameters = {'bootstrap': True,
                         'ccp_alpha': 0.0,
                         'class_weight': None,
                         'criterion': 'gini',
                         'max_depth': 20,
                         'max_features': 3,
                         'max_leaf_nodes': None,
                         'max_samples': None,
                         'min_impurity_decrease': 0.0,
                         'min_impurity_split': None,
                         'min_samples_leaf': 1,
                         'min_samples_split': 2,
                         'min_weight_fraction_leaf': 0.0,
                         'n_estimators': 20,
                         'n_jobs': -1,
                         'oob_score': False,
                         'random_state': 32,
                         'verbose': 0,
                         'warm_start': False}


    n_estimators = 20
    max_depth = 20
    max_features = 3
    random_state = 32
    n_jobs = -1
    test_model = md.train_model(df_train_X, train_Y, n_estimators, max_depth, max_features, random_state, n_jobs)

    test_parameters = test_model.get_params()

    assert type(test_model) == sklearn.ensemble._forest.RandomForestClassifier

    assert test_parameters == actual_parameters

    test_X = [[12.        ,  1.        ,  7.        ,  0.        , 92.        ,
                96.        ,  7.        , 11.        , 46.26785714, 17.03523035,
                32.06775068,  1.        ,  1.        ],
               [12.        ,  8.        ,  7.        ,  0.        , 92.        ,
                96.        ,  8.        , 11.        , 46.26785714, 17.03523035,
                32.06775068,  1.        ,  1.        ],
               [12.        ,  8.        ,  7.        ,  0.        , 92.        ,
                96.        ,  6.        ,  9.        , 46.26785714, 17.03523035,
                32.06775068,  1.        ,  1.        ],
               [ 4.        , 21.        ,  7.        ,  0.        , 92.        ,
                96.        ,  8.        , 11.        , 46.26785714, 17.03523035,
                32.06775068,  1.        ,  1.        ],
               [ 4.        ,  7.        ,  7.        ,  0.        , 92.        ,
                96.        ,  6.        ,  9.        , 46.26785714, 17.03523035,
                32.06775068,  1.        ,  1.        ],
               [ 4.        , 28.        ,  7.        ,  0.        , 92.        ,
                96.        ,  6.        ,  9.        , 46.26785714, 17.03523035,
                32.06775068,  1.        ,  1.        ]]
    
    df_test_X = pd.DataFrame(test_X, columns = input_X_cols)

    actual_predictions = [1, 2, 1, 1, 1, 0]

    test_predictions = md.make_prediction(test_model, df_test_X)

    assert all(actual_predictions == test_predictions) == True

def test_make_prediction_unhappy():
    train_X = [[1, 1, 7, 'AA', 'JFK', 'LAX', 8, 11, 46.26785714285714,
                17.035230352303525, 32.06775067750677, 1.0, 1.0],
               [1, 8, 7, 'AA', 'JFK', 'LAX', 8, 11, 46.26785714285714,
                17.035230352303525, 32.06775067750677, 1.0, 1.0],
               [1, 22, 7, 'AA', 'JFK', 'LAX', 8, 11, 46.26785714285714,
                17.035230352303525, 32.06775067750677, 1.0, 1.0],
               [1, 29, 7, 'AA', 'JFK', 'LAX', 8, 11, 46.26785714285714,
                17.035230352303525, 32.06775067750677, 1.0, 1.0],
               [1, 1, 7, 'AA', 'JFK', 'LAX', 7, 10, 46.26785714285714,
                17.035230352303525, 32.06775067750677, 1.0, 1.0],
               [1, 8, 7, 'AA', 'JFK', 'LAX', 7, 10, 46.26785714285714,
                17.035230352303525, 32.06775067750677, 1.0, 1.0],
               [1, 29, 7, 'AA', 'JFK', 'LAX', 7, 10, 46.26785714285714,
                17.035230352303525, 32.06775067750677, 1.0, 1.0],
               [12, 23, 7, 'AA', 'JFK', 'LAX', 8, 11, 46.26785714285714,
                17.035230352303525, 32.06775067750677, 1.0, 1.0]]

    input_X_cols = ['Month', 'DayofMonth', 'DayOfWeek', 'Reporting_Airline', 'Origin', 'Dest', 'DepTime_blk', 
                    'ArrTime_blk', 'avg_org_day_airline', 'avg_org_time_airline', 'avg_dest_time_airline', 
                    'f_int_origin', 'f_int_dest'] 

    df_train_X = pd.DataFrame(train_X, columns = input_X_cols)

    train_Y = [2, 2, 1, 0, 1, 1, 0, 0]

    n_estimators = 20
    max_depth = 20
    max_features = 3
    random_state = 32
    n_jobs = -1
    test_model = md.train_model(df_train_X, train_Y, n_estimators, max_depth, max_features, random_state, n_jobs)

    assert test_model is None

    test_X = [[12.        ,  1.        ,  7.        ,  0.        , 92.        ,
                96.        ,  7.        , 11.        , 46.26785714, 17.03523035,
                32.06775068,  1.        ,  1.        ],
               [12.        ,  8.        ,  7.        ,  0.        , 92.        ,
                96.        ,  8.        , 11.        , 46.26785714, 17.03523035,
                32.06775068,  1.        ,  1.        ],
               [12.        ,  8.        ,  7.        ,  0.        , 92.        ,
                96.        ,  6.        ,  9.        , 46.26785714, 17.03523035,
                32.06775068,  1.        ,  1.        ],
               [ 4.        , 21.        ,  7.        ,  0.        , 92.        ,
                96.        ,  8.        , 11.        , 46.26785714, 17.03523035,
                32.06775068,  1.        ,  1.        ],
               [ 4.        ,  7.        ,  7.        ,  0.        , 92.        ,
                96.        ,  6.        ,  9.        , 46.26785714, 17.03523035,
                32.06775068,  1.        ,  1.        ],
               [ 4.        , 28.        ,  7.        ,  0.        , 92.        ,
                96.        ,  6.        ,  9.        , 46.26785714, 17.03523035,
                32.06775068,  1.        ,  1.        ]]
    
    df_test_X = pd.DataFrame(test_X, columns = input_X_cols)

    test_predictions = md.make_prediction(test_model, df_test_X)

    assert test_predictions is None

def test_score_model_happy():
    predictions = [1, 2, 1, 1, 1, 0]

    test_Y = [2, 2, 1, 0, 0, 1]

    actual_string = 'F1-score: 0.3333333333333333'

    average = 'weighted'

    test_string = md.score_model(predictions, test_Y, average)

    assert actual_string == test_string

def test_score_model_unhappy():
    predictions = ['1', '2', '1', "1", '1', '0']

    test_Y = [2, 2, 1, 0, 0, 1]

    average = 'weighted'

    test_string = md.score_model(predictions, test_Y, average)

    assert test_string is None


def run_modeling_tests():
    logger.debug('Testing functions from modeling script')

    logger.debug('Testing happy path on create_train_test')
    create_train_test_happy()

    logger.debug('Testing unhappy path on create_train_test')
    create_train_test_unhappy()

    logger.debug('Testing train model function as part of testing make prediction function')

    logger.debug('Testing happy path on make_prediction')
    test_make_prediction_happy()

    logger.debug('Testing unhappy path on make_prediction')
    test_make_prediction_unhappy()

    logger.debug('Testing happy path on score_model')
    test_score_model_happy()

    logger.debug('Testing unhappy path on score_model')
    test_score_model_unhappy()













