import src.generate_features as gf
import pandas as pd
import logging

logger = logging.getLogger('test_generate_features')

def flag_international_airports_happy():

    inputs = [['Akron', 'Akron Executive Airport', 'AKC', 'Non-Hub/Reliever',
              'No Commercial Service'],
             ['Albany', 'Albany International Airport', 'ALB', 'Small',
              '2,848,000\xa0[2]'],
             ['Albuquerque', 'Albuquerque International Sunport', 'ABQ',
              'Medium', '5,258,775\xa0[3]'],
             ['Anchorage', 'Ted Stevens Anchorage International Airport',
              'ANC', 'Medium', '5,176,371[4]'],
             ['Appleton', 'Appleton International Airport', 'ATW', 'Small',
              '717,757\xa0[5]']]

    input_cols = ['Location', 'Airport', 'IATA code', 'Passenger role', '2018 passengers']

    df_input = pd.DataFrame(inputs, columns = input_cols)

    actual = [['AKC', 1], ['ALB', 1], ['ABQ', 1], ['ANC', 1], ['ATW', 1]]

    actual_cols = ['Origin', 'f_international']

    df_true = pd.DataFrame(actual, columns = actual_cols)

    variable = 'f_international'
    columns = ['IATA code', 'f_international']
    old = 'IATA code'
    new = 'Origin'

    df_test = gf.flag_international_airports(df_input, variable, columns, old, new)

    assert df_test.equals(df_true)

def flag_international_airports_unhappy():
    inputs = [['Akron', 'Akron Executive Airport', 'AKC', 'Non-Hub/Reliever',
              'No Commercial Service'],
             ['Albany', 'Albany International Airport', 'ALB', 'Small',
              '2,848,000\xa0[2]'],
             ['Albuquerque', 'Albuquerque International Sunport', 'ABQ',
              'Medium', '5,258,775\xa0[3]'],
             ['Anchorage', 'Ted Stevens Anchorage International Airport',
              'ANC', 'Medium', '5,176,371[4]'],
             ['Appleton', 'Appleton International Airport', 'ATW', 'Small',
              '717,757\xa0[5]']]

    input_cols = ['Location', 'Airport', 'IATA code', 'Passenger role', '2018 passengers']

    df_input = pd.DataFrame(inputs, columns = input_cols)

    actual = [['Akron', 'Akron Executive Airport', 'AKC', 'Non-Hub/Reliever',
              'No Commercial Service', 1],
             ['Albany', 'Albany International Airport', 'ALB', 'Small',
              '2,848,000\xa0[2]', 1],
             ['Albuquerque', 'Albuquerque International Sunport', 'ABQ',
              'Medium', '5,258,775\xa0[3]', 1],
             ['Anchorage', 'Ted Stevens Anchorage International Airport',
              'ANC', 'Medium', '5,176,371[4]', 1],
             ['Appleton', 'Appleton International Airport', 'ATW', 'Small',
              '717,757\xa0[5]', 1]]

    actual_cols = ['Location','Airport','Origin','Passenger role','2018 passengers',
                   'f_international']

    df_true = pd.DataFrame(actual, columns = actual_cols)

    variable = 'f_international'
    columns = ['IATA codeWRONG', 'f_international']
    old = 'IATA code'
    new = 'Origin'

    df_test = gf.flag_international_airports(df_input, variable, columns, old, new)

    assert df_test.equals(df_true)

def convert_str_happy():
    inputs = [['2017-01-11', 2017, 1, 11, 3, 'AA', 'JFK', 'LAX', 800, 1141,
                18.0, 0.0, 0.0, 1.0, 8, 11, 'On-time', 'Morning', 'Morning'],
               ['2017-01-12', 2017, 1, 12, 4, 'AA', 'JFK', 'LAX', 800, 1141,
                12.0, 0.0, 0.0, 1.0, 8, 11, 'On-time', 'Morning', 'Morning'],
               ['2017-01-13', 2017, 1, 13, 5, 'AA', 'JFK', 'LAX', 800, 1141,
                -26.0, 0.0, 0.0, 1.0, 8, 11, 'On-time', 'Morning', 'Morning'],
               ['2017-01-15', 2017, 1, 15, 7, 'AA', 'JFK', 'LAX', 800, 1141,
                23.0, 0.0, 0.0, 1.0, 8, 11, 'On-time', 'Morning', 'Morning'],
               ['2017-01-16', 2017, 1, 16, 1, 'AA', 'JFK', 'LAX', 800, 1141,
                13.0, 0.0, 0.0, 1.0, 8, 11, 'On-time', 'Morning', 'Morning']]

    input_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                  'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 
                  'ArrDelay', 'Cancelled', 'Diverted', 'Flights', 'DepTime_blk', 
                  'ArrTime_blk', 'Delay_group', 'DepTime_cat', 'ArrTime_cat']

    df_input = pd.DataFrame(inputs, columns = input_cols)

    actual = [['2017-01-11', 2017, 1, 11, '3', 'AA', 'JFK', 'LAX', 800, 1141,
                18.0, 0.0, 0.0, 1.0, 8, 11, 'On-time', 'Morning', 'Morning'],
               ['2017-01-12', 2017, 1, 12, '4', 'AA', 'JFK', 'LAX', 800, 1141,
                12.0, 0.0, 0.0, 1.0, 8, 11, 'On-time', 'Morning', 'Morning'],
               ['2017-01-13', 2017, 1, 13, '5', 'AA', 'JFK', 'LAX', 800, 1141,
                -26.0, 0.0, 0.0, 1.0, 8, 11, 'On-time', 'Morning', 'Morning'],
               ['2017-01-15', 2017, 1, 15, '7', 'AA', 'JFK', 'LAX', 800, 1141,
                23.0, 0.0, 0.0, 1.0, 8, 11, 'On-time', 'Morning', 'Morning'],
               ['2017-01-16', 2017, 1, 16, '1', 'AA', 'JFK', 'LAX', 800, 1141,
                13.0, 0.0, 0.0, 1.0, 8, 11, 'On-time', 'Morning', 'Morning']]

    actual_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                  'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 
                  'ArrDelay', 'Cancelled', 'Diverted', 'Flights', 'DepTime_blk', 
                  'ArrTime_blk', 'Delay_group', 'DepTime_cat', 'ArrTime_cat']

    df_true = pd.DataFrame(actual, columns = actual_cols)

    variable = 'DayOfWeek'

    df_test = gf.convert_str(df_input, variable)

    assert df_test.equals(df_true)

def convert_str_unhappy():
    inputs = [['2017-01-11', 2017, 1, 11, 3, 'AA', 'JFK', 'LAX', 800, 1141,
                18.0, 0.0, 0.0, 1.0, 8, 11, 'On-time', 'Morning', 'Morning'],
               ['2017-01-12', 2017, 1, 12, 4, 'AA', 'JFK', 'LAX', 800, 1141,
                12.0, 0.0, 0.0, 1.0, 8, 11, 'On-time', 'Morning', 'Morning'],
               ['2017-01-13', 2017, 1, 13, 5, 'AA', 'JFK', 'LAX', 800, 1141,
                -26.0, 0.0, 0.0, 1.0, 8, 11, 'On-time', 'Morning', 'Morning'],
               ['2017-01-15', 2017, 1, 15, 7, 'AA', 'JFK', 'LAX', 800, 1141,
                23.0, 0.0, 0.0, 1.0, 8, 11, 'On-time', 'Morning', 'Morning'],
               ['2017-01-16', 2017, 1, 16, 1, 'AA', 'JFK', 'LAX', 800, 1141,
                13.0, 0.0, 0.0, 1.0, 8, 11, 'On-time', 'Morning', 'Morning']]

    input_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                  'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 
                  'ArrDelay', 'Cancelled', 'Diverted', 'Flights', 'DepTime_blk', 
                  'ArrTime_blk', 'Delay_group', 'DepTime_cat', 'ArrTime_cat']

    df_input = pd.DataFrame(inputs, columns = input_cols)

    actual = [['2017-01-11', 2017, 1, 11, 3, 'AA', 'JFK', 'LAX', 800, 1141,
              18.0, 0.0, 0.0, 1.0, 8, 11, 'On-time', 'Morning', 'Morning'],
             ['2017-01-12', 2017, 1, 12, 4, 'AA', 'JFK', 'LAX', 800, 1141,
              12.0, 0.0, 0.0, 1.0, 8, 11, 'On-time', 'Morning', 'Morning'],
             ['2017-01-13', 2017, 1, 13, 5, 'AA', 'JFK', 'LAX', 800, 1141,
              -26.0, 0.0, 0.0, 1.0, 8, 11, 'On-time', 'Morning', 'Morning'],
             ['2017-01-15', 2017, 1, 15, 7, 'AA', 'JFK', 'LAX', 800, 1141,
              23.0, 0.0, 0.0, 1.0, 8, 11, 'On-time', 'Morning', 'Morning'],
             ['2017-01-16', 2017, 1, 16, 1, 'AA', 'JFK', 'LAX', 800, 1141,
              13.0, 0.0, 0.0, 1.0, 8, 11, 'On-time', 'Morning', 'Morning']]

    actual_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 
                  'Reporting_Airline', 'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 
                  'ArrDelay', 'Cancelled', 'Diverted', 'Flights', 'DepTime_blk', 
                  'ArrTime_blk', 'Delay_group', 'DepTime_cat', 'ArrTime_cat']

    df_true = pd.DataFrame(actual, columns = actual_cols)

    variable = 'DayOfWeekWRONG'

    df_test = gf.convert_str(df_input, variable)

    assert df_test.equals(df_true)

def calculate_flight_averages_happy():
    inputs = [['2019-12-31', '2', 'DTW', 'ORD', 'DL', 1.0, 'Night', 'Night'],
              ['2019-12-31', '2', 'MSP', 'ORD', 'DL', 1.0, 'Night', 'Night'],
              ['2019-12-31', '2', 'ATL', 'ORD', 'DL', 1.0, 'Night', 'Night'],
              ['2017-01-01', '7', 'ATL', 'ORD', 'DL', 1.0, 'Night', 'Night'],
              ['2017-01-01', '7', 'ATL', 'ORD', 'DL', 1.0, 'Afternoon/Evening',
               'Night'],
              ['2019-01-30', '3', 'SEA', 'ORD', 'DL', 1.0, 'Afternoon/Evening',
               'Night'],
              ['2019-01-30', '3', 'ATL', 'ORD', 'DL', 1.0, 'Afternoon/Evening',
               'Night'],
              ['2019-01-30', '3', 'ATL', 'ORD', 'DL', 1.0, 'Night', 'Night'],
              ['2019-01-30', '3', 'DTW', 'ORD', 'DL', 1.0, 'Night', 'Night']]

    input_cols = ['FlightDate', 'DayOfWeek', 'Origin', 'Dest', 'Reporting_Airline', 
                  'Flights', 'DepTime_cat', 'ArrTime_cat']

    df_input = pd.DataFrame(inputs, columns = input_cols)

    actual = [['ORD', 'DL', 'Night', 3.0]]

    actual_cols = ['Dest', 'Reporting_Airline', 'ArrTime_cat', 'avg_dest_time_airline']

    df_true = pd.DataFrame(actual, columns = actual_cols)

    sum_columns = ['FlightDate','Dest','Reporting_Airline', 'ArrTime_cat']
    avg_columns = ['Dest','Reporting_Airline','ArrTime_cat']
    new = 'avg_dest_time_airline'

    df_test = gf.calculate_flight_averages(df_input, sum_columns, avg_columns, new)

    assert df_test.equals(df_true)

def calculate_flight_averages_unhappy():
    inputs = [['2019-12-31', '2', 'DTW', 'ORD', 'DL', 1.0, 'Night', 'Night'],
              ['2019-12-31', '2', 'MSP', 'ORD', 'DL', 1.0, 'Night', 'Night'],
              ['2019-12-31', '2', 'ATL', 'ORD', 'DL', 1.0, 'Night', 'Night'],
              ['2017-01-01', '7', 'ATL', 'ORD', 'DL', 1.0, 'Night', 'Night'],
              ['2017-01-01', '7', 'ATL', 'ORD', 'DL', 1.0, 'Afternoon/Evening',
               'Night'],
              ['2019-01-30', '3', 'SEA', 'ORD', 'DL', 1.0, 'Afternoon/Evening',
               'Night'],
              ['2019-01-30', '3', 'ATL', 'ORD', 'DL', 1.0, 'Afternoon/Evening',
               'Night'],
              ['2019-01-30', '3', 'ATL', 'ORD', 'DL', 1.0, 'Night', 'Night'],
              ['2019-01-30', '3', 'DTW', 'ORD', 'DL', 1.0, 'Night', 'Night']]

    input_cols = ['FlightDate', 'DayOfWeek', 'Origin', 'Dest', 'Reporting_Airline', 
                  'Flights', 'DepTime_cat', 'ArrTime_cat']

    df_input = pd.DataFrame(inputs, columns = input_cols)

    actual = [['ORD', 'DL', 'Night', 1.0]]

    actual_cols = ['Dest', 'Reporting_Airline', 'ArrTime_cat', 'avg_dest_time_airline']

    df_true = pd.DataFrame(actual, columns = actual_cols)

    sum_columns = ['FlightDate','Dest','Reporting_Airline', 'ArrTime_catWRONG']
    avg_columns = ['Dest','Reporting_Airline','ArrTime_cat']
    new = 'avg_dest_time_airline'

    df_test = gf.calculate_flight_averages(df_input, sum_columns, avg_columns, new)

    assert df_test.equals(df_true)

def merge_features_happy():

    inputs = [['2019-12-31', '2', 'DTW', 'ORD', 'DL', 1.0, 'Night', 'Night'],
              ['2019-12-31', '2', 'MSP', 'ORD', 'DL', 1.0, 'Night', 'Night'],
              ['2019-12-31', '2', 'ATL', 'ORD', 'DL', 1.0, 'Night', 'Night'],
              ['2017-01-01', '7', 'ATL', 'ORD', 'DL', 1.0, 'Night', 'Night'],
              ['2017-01-01', '7', 'ATL', 'ORD', 'DL', 1.0, 'Afternoon/Evening',
               'Night'],
              ['2019-01-30', '3', 'SEA', 'ORD', 'DL', 1.0, 'Afternoon/Evening',
               'Night'],
              ['2019-01-30', '3', 'ATL', 'ORD', 'DL', 1.0, 'Afternoon/Evening',
               'Night'],
              ['2019-01-30', '3', 'ATL', 'ORD', 'DL', 1.0, 'Night', 'Night'],
              ['2019-01-30', '3', 'DTW', 'ORD', 'DL', 1.0, 'Night', 'Night']]

    input_cols = ['FlightDate', 'DayOfWeek', 'Origin', 'Dest', 'Reporting_Airline', 
                  'Flights', 'DepTime_cat', 'ArrTime_cat']

    df_input = pd.DataFrame(inputs, columns = input_cols)

    subset = [['ORD', 'DL', 'Night', 3.0]]

    subset_cols = ['Dest', 'Reporting_Airline', 'ArrTime_cat', 'avg_dest_time_airline']

    df_subset = pd.DataFrame(subset, columns = subset_cols)
    
    actual = [['2019-12-31', '2', 'DTW', 'ORD', 'DL', 1.0, 'Night', 'Night',
              3.0],
             ['2019-12-31', '2', 'MSP', 'ORD', 'DL', 1.0, 'Night', 'Night',
              3.0],
             ['2019-12-31', '2', 'ATL', 'ORD', 'DL', 1.0, 'Night', 'Night',
              3.0],
             ['2017-01-01', '7', 'ATL', 'ORD', 'DL', 1.0, 'Night', 'Night',
              3.0],
             ['2017-01-01', '7', 'ATL', 'ORD', 'DL', 1.0, 'Afternoon/Evening',
              'Night', 3.0],
             ['2019-01-30', '3', 'SEA', 'ORD', 'DL', 1.0, 'Afternoon/Evening',
              'Night', 3.0],
             ['2019-01-30', '3', 'ATL', 'ORD', 'DL', 1.0, 'Afternoon/Evening',
              'Night', 3.0],
             ['2019-01-30', '3', 'ATL', 'ORD', 'DL', 1.0, 'Night', 'Night',
              3.0],
             ['2019-01-30', '3', 'DTW', 'ORD', 'DL', 1.0, 'Night', 'Night',
              3.0]]

    actual_cols = ['FlightDate', 'DayOfWeek', 'Origin', 'Dest', 'Reporting_Airline', 
                   'Flights', 'DepTime_cat', 'ArrTime_cat', 'avg_dest_time_airline']

    df_true = pd.DataFrame(actual, columns = actual_cols)

    method = 'inner'
    columns = ['Dest', 'Reporting_Airline', 'ArrTime_cat']

    df_test = gf.merge_features(df_input, df_subset, method, columns)

    assert df_test.equals(df_true)

def merge_features_unhappy():

    inputs = [['2019-12-31', '2', 'DTW', 'ORD', 'DL', 1.0, 'Night', 'Night'],
              ['2019-12-31', '2', 'MSP', 'ORD', 'DL', 1.0, 'Night', 'Night'],
              ['2019-12-31', '2', 'ATL', 'ORD', 'DL', 1.0, 'Night', 'Night'],
              ['2017-01-01', '7', 'ATL', 'ORD', 'DL', 1.0, 'Night', 'Night'],
              ['2017-01-01', '7', 'ATL', 'ORD', 'DL', 1.0, 'Afternoon/Evening',
               'Night'],
              ['2019-01-30', '3', 'SEA', 'ORD', 'DL', 1.0, 'Afternoon/Evening',
               'Night'],
              ['2019-01-30', '3', 'ATL', 'ORD', 'DL', 1.0, 'Afternoon/Evening',
               'Night'],
              ['2019-01-30', '3', 'ATL', 'ORD', 'DL', 1.0, 'Night', 'Night'],
              ['2019-01-30', '3', 'DTW', 'ORD', 'DL', 1.0, 'Night', 'Night']]

    input_cols = ['FlightDate', 'DayOfWeek', 'Origin', 'Dest', 'Reporting_Airline', 
                  'Flights', 'DepTime_cat', 'ArrTime_cat']

    df_input = pd.DataFrame(inputs, columns = input_cols)

    subset = [['ORD', 'DL', 'Night', 3.0]]

    subset_cols = ['Dest', 'Reporting_Airline', 'ArrTime_cat', 'avg_dest_time_airline']

    df_subset = pd.DataFrame(subset, columns = subset_cols)

    actual = [['2019-12-31', '2', 'DTW', 'ORD', 'DL', 1.0, 'Night', 'Night'],
             ['2019-12-31', '2', 'MSP', 'ORD', 'DL', 1.0, 'Night', 'Night'],
             ['2019-12-31', '2', 'ATL', 'ORD', 'DL', 1.0, 'Night', 'Night'],
             ['2017-01-01', '7', 'ATL', 'ORD', 'DL', 1.0, 'Night', 'Night'],
             ['2017-01-01', '7', 'ATL', 'ORD', 'DL', 1.0, 'Afternoon/Evening',
              'Night'],
             ['2019-01-30', '3', 'SEA', 'ORD', 'DL', 1.0, 'Afternoon/Evening',
              'Night'],
             ['2019-01-30', '3', 'ATL', 'ORD', 'DL', 1.0, 'Afternoon/Evening',
              'Night'],
             ['2019-01-30', '3', 'ATL', 'ORD', 'DL', 1.0, 'Night', 'Night'],
             ['2019-01-30', '3', 'DTW', 'ORD', 'DL', 1.0, 'Night', 'Night']]

    actual_cols = ['FlightDate', 'DayOfWeek', 'Origin', 'Dest', 'Reporting_Airline', 
                   'Flights', 'DepTime_cat', 'ArrTime_cat']

    df_true = pd.DataFrame(actual, columns = actual_cols)

    method = 'inner'
    columns = ['Dest', 'Reporting_Airline', 'ArrTime_catWRONG']

    df_test = gf.merge_features(df_input, df_subset, method, columns)

    assert df_test.equals(df_true)

def run_generate_features_tests():
    logger.debug('Testing functions from generate_features script')

    logger.debug('Testing happy path on flag_international_airports')
    flag_international_airports_happy()

    logger.debug('Testing unhappy path on flag_international_airports')
    flag_international_airports_unhappy()

    logger.debug('Testing happy path on convert_str')
    convert_str_happy()

    logger.debug('Testing unhappy path on convert_str')
    convert_str_unhappy()

    logger.debug('Testing happy path on calculate_flight_averages')
    calculate_flight_averages_happy()

    logger.debug('Testing unhappy path on calculate_flight_averages')
    calculate_flight_averages_happy()

    logger.debug('Testing happy path on merge_features')
    merge_features_happy()

    logger.debug('Testing unhappy path on merge_features')
    merge_features_unhappy()


