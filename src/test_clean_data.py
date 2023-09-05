import src.clean_data as cd
import pandas as pd
import logging

logger = logging.getLogger('test_clean_data')

def remove_observations_happy():
    """ Tests the remove_observations function for a happy path """
    inputs = [['2017-02-01', 2017, 2, 1, 3, 'DL', 'BOS', 'SLC', 1741, 
               2127, None, 0.0, 1.0, 1.0],
              ['2017-02-02', 2017, 2, 2, 4, 'DL', 'JAC', 'SLC', 1310, 
               1419, None, 1.0, 0.0, 1.0],
              ['2017-02-01', 2017, 2, 1, 3, 'DL', 'ATL', 'LAX', 1759, 
               1959, 178.0, 0.0, 0.0, 1.0],
              ['2017-02-16', 2017, 2, 16, 4, 'DL', 'MSP', 'ATL', 1515, 
               1848, -23.0, 0.0, 0.0, 1.0],
              ['2017-02-01', 2017, 2, 1, 3, 'DL', 'ATL', 'MSP', 830, 
               1013, -2.0, 0.0, 0.0, 1.0]]
    input_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                  'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 
                  'ArrDelay', 'Cancelled', 'Diverted', 'Flights']
    df_input = pd.DataFrame(inputs, columns = input_cols)

    actual = [['2017-02-01', 2017, 2, 1, 3, 'DL', 'ATL', 'LAX', 1759, 1959, 
               178.0, 0.0, 0.0, 1.0],
              ['2017-02-16', 2017, 2, 16, 4, 'DL', 'MSP', 'ATL', 1515, 1848, 
               -23.0, 0.0, 0.0, 1.0],
              ['2017-02-01', 2017, 2, 1, 3, 'DL', 'ATL', 'MSP', 830, 1013, 
               -2.0, 0.0, 0.0, 1.0]]

    actual_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                  'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 
                  'ArrDelay', 'Cancelled', 'Diverted', 'Flights']

    df_true = pd.DataFrame(actual, columns = actual_cols)

    columns = ['Cancelled', 'Diverted']
    df_test = cd.remove_observations(df_input, columns)
    df_test = df_test.reset_index(drop=True)

    assert df_test.equals(df_true)

def remove_observations_unhappy():
    inputs = [['2017-02-02', 2017, 2, 2, 4, 'DL', 'JAC', 'SLC', 1310, 1419, None,
               1.0, 0.0, 1.0],
              ['2017-02-28', 2017, 2, 28, 2, 'DL', 'BOS', 'JFK', 1930, 2059,
               None, 1.0, 0.0, 1.0],
              ['2017-02-28', 2017, 2, 28, 2, 'DL', 'ATL', 'EGE', 1040, 1223,
               None, 1.0, 0.0, 1.0],
              ['2017-02-28', 2017, 2, 28, 2, 'DL', 'EGE', 'ATL', 1313, 1819,
               None, 1.0, 0.0, 1.0],
              ['2017-02-07', 2017, 2, 7, 2, 'DL', 'JAC', 'SLC', 700, 823, None,
               1.0, 0.0, 1.0]]
    input_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                  'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 
                  'ArrDelay', 'Cancelled', 'Diverted', 'Flights']
    df_input = pd.DataFrame(inputs, columns = input_cols)

    actual = []

    actual_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                  'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 
                  'ArrDelay', 'Cancelled', 'Diverted', 'Flights']

    df_true = pd.DataFrame(actual, columns = actual_cols)

    columns = ['Cancelled', 'Diverted']
    df_test = cd.remove_observations(df_input, columns)

    assert df_true.empty & df_test.empty

def create_hour_block_happy():
    inputs = [['2017-02-01', 2017, 2, 1, 3, 'DL', 'ATL', 'BOS', 730, 1000, -1.0,
                0.0, 0.0, 1.0],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'ATL', 'LAX', 720, 930, 16.0,
                0.0, 0.0, 1.0],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'MCO', 'MIA', 700, 759, -3.0,
                0.0, 0.0, 1.0],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'ATL', 'MSP', 830, 1013, -2.0,
                0.0, 0.0, 1.0],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'JFK', 'LAX', 710, 1040, 11.0,
                0.0, 0.0, 1.0]]

    input_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                  'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 
                  'ArrDelay', 'Cancelled', 'Diverted', 'Flights']

    df_input = pd.DataFrame(inputs, columns = input_cols)

    actual = [['2017-02-01', 2017, 2, 1, 3, 'DL', 'ATL', 'BOS', '730', '1000',
                -1.0, 0.0, 0.0, 1.0, 7, 10],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'ATL', 'LAX', '720', '930',
                16.0, 0.0, 0.0, 1.0, 7, 9],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'MCO', 'MIA', '700', '759',
                -3.0, 0.0, 0.0, 1.0, 7, 7],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'ATL', 'MSP', '830', '1013',
                -2.0, 0.0, 0.0, 1.0, 8, 10],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'JFK', 'LAX', '710', '1040',
                11.0, 0.0, 0.0, 1.0, 7, 10]]

    actual_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                  'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 
                  'ArrDelay', 'Cancelled', 'Diverted', 'Flights', 'DepTime_blk', 'ArrTime_blk']

    df_true = pd.DataFrame(actual, columns = actual_cols)

    old = ['CRSDepTime', 'CRSArrTime']
    new = ['DepTime_blk', 'ArrTime_blk']

    df_test = cd.create_hour_block(df_input, old, new)

    assert df_test.equals(df_true)

def create_hour_block_unhappy():
    inputs = [['2017-02-01', 2017, 2, 1, 3, 'DL', 'GSP', 'ATL', 50830, 935, -9.0,
                0.0, 0.0, 1.0],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'BNA', 'ATL', 4800, 1014,
                -15.0, 0.0, 0.0, 1.0],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'DFW', 'ATL', 1445, 1750,
                -4.0, 0.0, 0.0, 1.0],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'ATL', 'DFW', 1615, 1750,
                -23.0, 0.0, 0.0, 1.0],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'SJC', 'LAX', 9609, 740, -7.0,
                0.0, 0.0, 1.0]]

    input_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                  'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 
                  'ArrDelay', 'Cancelled', 'Diverted', 'Flights']

    df_input = pd.DataFrame(inputs, columns = input_cols)

    actual = [['2017-02-01', 2017, 2, 1, 3, 'DL', 'GSP', 'ATL', '50830', '935',
                -9.0, 0.0, 0.0, 1.0, 508, 9],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'BNA', 'ATL', '4800', '1014',
                -15.0, 0.0, 0.0, 1.0, 48, 10],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'DFW', 'ATL', '1445', '1750',
                -4.0, 0.0, 0.0, 1.0, 14, 17],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'ATL', 'DFW', '1615', '1750',
                -23.0, 0.0, 0.0, 1.0, 16, 17],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'SJC', 'LAX', '9609', '740',
                -7.0, 0.0, 0.0, 1.0, 96, 7]]

    actual_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                  'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 
                  'ArrDelay', 'Cancelled', 'Diverted', 'Flights', 'DepTime_blk', 'ArrTime_blk']

    df_true = pd.DataFrame(actual, columns = actual_cols)

    old = ['CRSDepTime', 'CRSArrTime']
    new = ['DepTime_blk', 'ArrTime_blk']

    df_test = cd.create_hour_block(df_input, old, new)

    assert df_test.equals(df_true)

def create_delay_category_happy():
    inputs = [['2017-02-15', 2017, 2, 15, 3, 'DL', 'DTW', 'DEN', '1218', '1347',
                -32.0, 0.0, 0.0, 1.0, 12, 13],
               ['2017-02-15', 2017, 2, 15, 3, 'DL', 'ATL', 'RIC', '1920', '2055',
                -17.0, 0.0, 0.0, 1.0, 19, 20],
               ['2017-02-15', 2017, 2, 15, 3, 'DL', 'ATL', 'PIT', '1242', '1422',
                -9.0, 0.0, 0.0, 1.0, 12, 14],
               ['2017-02-15', 2017, 2, 15, 3, 'DL', 'PIT', 'ATL', '1512', '1719',
                -34.0, 0.0, 0.0, 1.0, 15, 17],
               ['2017-02-15', 2017, 2, 15, 3, 'DL', 'ATL', 'MDW', '1050', '1145',
                -11.0, 0.0, 0.0, 1.0, 10, 11]]

    input_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 'Reporting_Airline', 
                  'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 'ArrDelay', 'Cancelled', 'Diverted', 
                  'Flights', 'DepTime_blk', 'ArrTime_blk']

    df_input = pd.DataFrame(inputs, columns = input_cols)

    actual = [['2017-02-15', 2017, 2, 15, 3, 'DL', 'DTW', 'DEN', '1218', '1347',
                -32.0, 0.0, 0.0, 1.0, 12, 13, 'Early'],
               ['2017-02-15', 2017, 2, 15, 3, 'DL', 'ATL', 'RIC', '1920', '2055',
                -17.0, 0.0, 0.0, 1.0, 19, 20, 'On-time'],
               ['2017-02-15', 2017, 2, 15, 3, 'DL', 'ATL', 'PIT', '1242', '1422',
                -9.0, 0.0, 0.0, 1.0, 12, 14, 'On-time'],
               ['2017-02-15', 2017, 2, 15, 3, 'DL', 'PIT', 'ATL', '1512', '1719',
                -34.0, 0.0, 0.0, 1.0, 15, 17, 'Early'],
               ['2017-02-15', 2017, 2, 15, 3, 'DL', 'ATL', 'MDW', '1050', '1145',
                -11.0, 0.0, 0.0, 1.0, 10, 11, 'On-time']]

    actual_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                   'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 
                   'ArrDelay', 'Cancelled', 'Diverted', 'Flights', 'DepTime_blk', 'ArrTime_blk', 
                   'Delay_group']

    df_true = pd.DataFrame(actual, columns = actual_cols)

    old = 'ArrDelay'
    new = 'Delay_group'
    values = ['Early', 'On-time', 'Late']

    df_test = cd.create_delay_category(df_input, old, new, values)

    assert df_test.equals(df_true)

def create_delay_category_unhappy():

    inputs = [['2017-02-01', 2017, 2, 1, 3, 'DL', 'PIT', 'ATL', '1745', '1943',
                '-21.0', 0.0, 0.0, 1.0, 17, 19],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'BOS', 'ATL', '545', '857',
                55.0, 0.0, 0.0, 1.0, 5, 8],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'ATL', 'DTW', '1458', '1702',
                '9.0', 0.0, 0.0, 1.0, 14, 17],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'ATL', 'BOS', '2125', '2358',
                -16.0, 0.0, 0.0, 1.0, 21, 23],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'LGA', 'ATL', '700', '944',
                -21.0, 0.0, 0.0, 1.0, 7, 9]]

    input_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 'Reporting_Airline', 
                  'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 'ArrDelay', 'Cancelled', 'Diverted', 
                  'Flights', 'DepTime_blk', 'ArrTime_blk']

    df_input = pd.DataFrame(inputs, columns = input_cols)

    actual = [['2017-02-01', 2017, 2, 1, 3, 'DL', 'PIT', 'ATL', '1745', '1943',
                '-21.0', 0.0, 0.0, 1.0, 17, 19, None],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'BOS', 'ATL', '545', '857',
                55.0, 0.0, 0.0, 1.0, 5, 8, None],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'ATL', 'DTW', '1458', '1702',
                '9.0', 0.0, 0.0, 1.0, 14, 17, None],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'ATL', 'BOS', '2125', '2358',
                -16.0, 0.0, 0.0, 1.0, 21, 23, None],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'LGA', 'ATL', '700', '944',
                -21.0, 0.0, 0.0, 1.0, 7, 9, None]]

    actual_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                   'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 
                   'ArrDelay', 'Cancelled', 'Diverted', 'Flights', 'DepTime_blk', 'ArrTime_blk', 
                   'Delay_group']

    df_true = pd.DataFrame(actual, columns = actual_cols)

    old = 'ArrDelay'
    new = 'Delay_group'
    values = ['Early', 'On-time', 'Late']

    df_test = cd.create_delay_category(df_input, old, new, values)

    assert df_test.equals(df_true)

def create_time_category_happy():
    inputs = [['2017-02-01', 2017, 2, 1, 3, 'DL', 'MSP', 'DTW', '2005', '2302',
                -10.0, 0.0, 0.0, 1.0, 20, 23, 'On-time'],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'SLC', 'ATL', '1655', '2231',
                -9.0, 0.0, 0.0, 1.0, 16, 22, 'On-time'],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'LGA', 'MSP', '1825', '2054',
                -27.0, 0.0, 0.0, 1.0, 18, 20, 'On-time'],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'ATL', 'DAB', '2231', '2350',
                -10.0, 0.0, 0.0, 1.0, 22, 23, 'On-time'],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'LAS', 'DTW', '2255', '553',
                -42.0, 0.0, 0.0, 1.0, 22, 5, 'Early']]

    input_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 'Reporting_Airline', 
                  'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 'ArrDelay', 'Cancelled', 'Diverted', 
                  'Flights', 'DepTime_blk', 'ArrTime_blk', 'Delay_group']

    df_input = pd.DataFrame(inputs, columns = input_cols)

    actual = [['2017-02-01', 2017, 2, 1, 3, 'DL', 'MSP', 'DTW', '2005', '2302',
                -10.0, 0.0, 0.0, 1.0, 20, 23, 'On-time', 'Night', 'Night'],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'SLC', 'ATL', '1655', '2231',
                -9.0, 0.0, 0.0, 1.0, 16, 22, 'On-time', 'Afternoon/Evening',
                'Night'],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'LGA', 'MSP', '1825', '2054',
                -27.0, 0.0, 0.0, 1.0, 18, 20, 'On-time', 'Afternoon/Evening',
                'Night'],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'ATL', 'DAB', '2231', '2350',
                -10.0, 0.0, 0.0, 1.0, 22, 23, 'On-time', 'Night', 'Night'],
               ['2017-02-01', 2017, 2, 1, 3, 'DL', 'LAS', 'DTW', '2255', '553',
                -42.0, 0.0, 0.0, 1.0, 22, 5, 'Early', 'Night', 'Morning']]
    
    actual_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                   'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 
                   'ArrDelay', 'Cancelled', 'Diverted', 'Flights', 'DepTime_blk', 'ArrTime_blk', 
                   'Delay_group', 'DepTime_cat', 'ArrTime_cat']

    df_true = pd.DataFrame(actual, columns = actual_cols)

    old = ['DepTime_blk', 'ArrTime_blk']
    new = ['DepTime_cat', 'ArrTime_cat']
    values = ['Morning', 'Afternoon/Evening', 'Night']

    df_test = cd.create_time_category(df_input, old, new, values)

    assert df_test.equals(df_true)

def create_time_category_unhappy():
    inputs = [['2017-02-02', 2017, 2, 2, 4, 'DL', 'RSW', 'DTW', '810', '1100',
                31.0, 0.0, 0.0, 1.0, None, 11, 'Late'],
               ['2017-02-02', 2017, 2, 2, 4, 'DL', 'LAX', 'JFK', '1605', '25',
                -1.0, 0.0, 0.0, 1.0, None, 0, 'On-time'],
               ['2017-02-02', 2017, 2, 2, 4, 'DL', 'CID', 'ATL', '540', '902',
                -27.0, 0.0, 0.0, 1.0, None, 9, 'On-time'],
               ['2017-02-02', 2017, 2, 2, 4, 'DL', 'MCO', 'LGA', '1535', '1814',
                -18.0, 0.0, 0.0, 1.0, None, 18, 'On-time'],
               ['2017-02-02', 2017, 2, 2, 4, 'DL', 'XNA', 'ATL', '600', '903',
                -30.0, 0.0, 0.0, 1.0, None, 9, 'On-time']]

    input_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 'Reporting_Airline', 
                  'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 'ArrDelay', 'Cancelled', 'Diverted', 
                  'Flights', 'DepTime_blk', 'ArrTime_blk', 'Delay_group']

    df_input = pd.DataFrame(inputs, columns = input_cols)

    actual = [['2017-02-02', 2017, 2, 2, 4, 'DL', 'RSW', 'DTW', '810', '1100',
                31.0, 0.0, 0.0, 1.0, None, 11, 'Late', None, 'Morning'],
               ['2017-02-02', 2017, 2, 2, 4, 'DL', 'LAX', 'JFK', '1605', '25',
                -1.0, 0.0, 0.0, 1.0, None, 0, 'On-time', None, 'Night'],
               ['2017-02-02', 2017, 2, 2, 4, 'DL', 'CID', 'ATL', '540', '902',
                -27.0, 0.0, 0.0, 1.0, None, 9, 'On-time', None, 'Morning'],
               ['2017-02-02', 2017, 2, 2, 4, 'DL', 'MCO', 'LGA', '1535', '1814',
                -18.0, 0.0, 0.0, 1.0, None, 18, 'On-time', None,
                'Afternoon/Evening'],
               ['2017-02-02', 2017, 2, 2, 4, 'DL', 'XNA', 'ATL', '600', '903',
                -30.0, 0.0, 0.0, 1.0, None, 9, 'On-time', None, 'Morning']]

    actual_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                   'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 
                   'ArrDelay', 'Cancelled', 'Diverted', 'Flights', 'DepTime_blk', 'ArrTime_blk', 
                   'Delay_group', 'DepTime_cat', 'ArrTime_cat']

    df_true = pd.DataFrame(actual, columns = actual_cols)

    old = ['DepTime_blk', 'ArrTime_blk']
    new = ['DepTime_cat', 'ArrTime_cat']
    values = ['Morning', 'Afternoon/Evening', 'Night']

    df_test = cd.create_time_category(df_input, old, new, values)

    assert df_test.equals(df_true)

def run_clean_data_tests():
    logger.debug('Testing functions from clean_data script')

    logger.debug('Testing happy path on remove_observations')
    remove_observations_happy()

    logger.debug('Testing unhappy path on remove_observations')
    remove_observations_unhappy()

    logger.debug('Testing happy path on create_hour_block')
    create_hour_block_happy()

    logger.debug('Testing unhappy path on create_hour_block')
    create_hour_block_unhappy()

    logger.debug('Testing happy path on create_delay_category_happy')
    create_delay_category_happy()

    logger.debug('Testing unhappy path on create_delay_category_happy')
    create_delay_category_unhappy()

    logger.debug('Testing happy path on create_time_category_happy')
    create_time_category_happy()

    logger.debug('Testing unhappy path on create_time_category_unhappy')
    create_time_category_unhappy()










