import src.helpers as hlp
import pandas as pd
import logging

logger = logging.getLogger('test_helpers')

def subset_happy():
    """ Tests the subset function for a happy path """
    inputs = [['2017-01-30', 2017, 1, 30, 1, 'AA', 'BOS', 'ORD', 1911, 2110,
                -33.0, 0.0, 0.0, 1.0, 19, 21, 'Early', 'Afternoon/Evening',
                'Night'],
               ['2017-01-31', 2017, 1, 31, 2, 'AA', 'BOS', 'ORD', 1911, 2110,
                -14.0, 0.0, 0.0, 1.0, 19, 21, 'On-time', 'Afternoon/Evening',
                'Night'],
               ['2017-01-01', 2017, 1, 1, 7, 'AA', 'ORD', 'SFO', 1335, 1621,
                19.0, 0.0, 0.0, 1.0, 13, 16, 'On-time', 'Afternoon/Evening',
                'Afternoon/Evening'],
               ['2017-01-02', 2017, 1, 2, 1, 'AA', 'ORD', 'SFO', 1335, 1621,
                39.0, 0.0, 0.0, 1.0, 13, 16, 'Late', 'Afternoon/Evening',
                'Afternoon/Evening'],
               ['2017-01-03', 2017, 1, 3, 2, 'AA', 'ORD', 'SFO', 1335, 1621,
                78.0, 0.0, 0.0, 1.0, 13, 16, 'Late', 'Afternoon/Evening',
                'Afternoon/Evening']]

    input_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                  'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 
                  'CRSArrTime', 'ArrDelay', 'Cancelled', 'Diverted', 'Flights', 
                  'DepTime_blk', 'ArrTime_blk', 'Delay_group', 'DepTime_cat', 
                  'ArrTime_cat']

    df_input = pd.DataFrame(inputs, columns = input_cols)

    actual = [['2017-01-30', 1, 'BOS', 'ORD', 'AA', 1.0, 'Afternoon/Evening',
                'Night'],
               ['2017-01-31', 2, 'BOS', 'ORD', 'AA', 1.0, 'Afternoon/Evening',
                'Night'],
               ['2017-01-01', 7, 'ORD', 'SFO', 'AA', 1.0, 'Afternoon/Evening',
                'Afternoon/Evening'],
               ['2017-01-02', 1, 'ORD', 'SFO', 'AA', 1.0, 'Afternoon/Evening',
                'Afternoon/Evening'],
               ['2017-01-03', 2, 'ORD', 'SFO', 'AA', 1.0, 'Afternoon/Evening',
                'Afternoon/Evening']]

    actual_cols = ['FlightDate', 'DayOfWeek', 'Origin', 'Dest', 'Reporting_Airline', 
                   'Flights', 'DepTime_cat', 'ArrTime_cat']

    df_true = pd.DataFrame(actual, columns = actual_cols)

    columns = ['FlightDate','DayOfWeek', 'Origin', 'Dest', 'Reporting_Airline', 
               'Flights', 'DepTime_cat','ArrTime_cat']

    df_test = hlp.subset(df_input, columns)

    assert df_test.equals(df_true)

def subset_unhappy():
    inputs = [['2017-01-30', 2017, 1, 30, 1, 'AA', 'BOS', 'ORD', 1911, 2110,
                -33.0, 0.0, 0.0, 1.0, 19, 21, 'Early', 'Afternoon/Evening',
                'Night'],
               ['2017-01-31', 2017, 1, 31, 2, 'AA', 'BOS', 'ORD', 1911, 2110,
                -14.0, 0.0, 0.0, 1.0, 19, 21, 'On-time', 'Afternoon/Evening',
                'Night'],
               ['2017-01-01', 2017, 1, 1, 7, 'AA', 'ORD', 'SFO', 1335, 1621,
                19.0, 0.0, 0.0, 1.0, 13, 16, 'On-time', 'Afternoon/Evening',
                'Afternoon/Evening'],
               ['2017-01-02', 2017, 1, 2, 1, 'AA', 'ORD', 'SFO', 1335, 1621,
                39.0, 0.0, 0.0, 1.0, 13, 16, 'Late', 'Afternoon/Evening',
                'Afternoon/Evening'],
               ['2017-01-03', 2017, 1, 3, 2, 'AA', 'ORD', 'SFO', 1335, 1621,
                78.0, 0.0, 0.0, 1.0, 13, 16, 'Late', 'Afternoon/Evening',
                'Afternoon/Evening']]

    input_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                  'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 
                  'CRSArrTime', 'ArrDelay', 'Cancelled', 'Diverted', 'Flights', 
                  'DepTime_blk', 'ArrTime_blk', 'Delay_group', 'DepTime_cat', 
                  'ArrTime_cat']

    df_input = pd.DataFrame(inputs, columns = input_cols)

    actual = [['2017-01-30', 2017, 1, 30, 1, 'AA', 'BOS', 'ORD', 1911, 2110,
              -33.0, 0.0, 0.0, 1.0, 19, 21, 'Early', 'Afternoon/Evening',
              'Night'],
             ['2017-01-31', 2017, 1, 31, 2, 'AA', 'BOS', 'ORD', 1911, 2110,
              -14.0, 0.0, 0.0, 1.0, 19, 21, 'On-time', 'Afternoon/Evening',
              'Night'],
             ['2017-01-01', 2017, 1, 1, 7, 'AA', 'ORD', 'SFO', 1335, 1621,
              19.0, 0.0, 0.0, 1.0, 13, 16, 'On-time', 'Afternoon/Evening',
              'Afternoon/Evening'],
             ['2017-01-02', 2017, 1, 2, 1, 'AA', 'ORD', 'SFO', 1335, 1621,
              39.0, 0.0, 0.0, 1.0, 13, 16, 'Late', 'Afternoon/Evening',
              'Afternoon/Evening'],
             ['2017-01-03', 2017, 1, 3, 2, 'AA', 'ORD', 'SFO', 1335, 1621,
              78.0, 0.0, 0.0, 1.0, 13, 16, 'Late', 'Afternoon/Evening',
              'Afternoon/Evening']]

    actual_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                   'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 
                   'CRSArrTime', 'ArrDelay', 'Cancelled', 'Diverted', 'Flights', 
                   'DepTime_blk', 'ArrTime_blk', 'Delay_group', 'DepTime_cat', 
                   'ArrTime_cat']

    df_true = pd.DataFrame(actual, columns = actual_cols)

    columns = ['FlightDateWRONG','DayOfWeek', 'Origin', 'Dest', 'Reporting_Airline', 
               'Flights', 'DepTime_cat','ArrTime_cat']

    df_test = hlp.subset(df_input, columns)

    assert df_test.equals(df_true)

def run_helper_tests():
    logger.debug('Testing functions from helpers script')

    logger.debug('Testing happy path on subset')
    subset_happy()

    logger.debug('Testing unhappy path on subset')
    subset_unhappy()












