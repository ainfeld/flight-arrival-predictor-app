import src.load_data as ld
import pandas as pd
import logging

logger = logging.getLogger('test_load_data')

def load_flight_data_happy():
    """ Tests the load_flight_data function for a happy path """
    inputs = [[2017, 2, 4, 1, 6, '2017-04-01', 'EV', 20366, 'EV', 'N907EV',
              2755, 10185, 1018502, 30185, 'AEX', 'Alexandria, LA', 'LA', 22,
              'Louisiana', 72, 11298, 1129804, 30194, 'DFW',
              'Dallas/Fort Worth, TX', 'TX', 48, 'Texas', 74, 1019, 1007.0,
              -12.0, 0.0, 0.0, -1.0, '1000-1059', 19.0, 1026.0, 1117.0, 9.0,
              1137, 1126.0, -11.0, 0.0, 0.0, -1.0, '1100-1159', 0.0, None, 0.0,
              78.0, 79.0, 51.0, 1.0, 285.0, 2, None, None, None, None, None, None,
              None, None, 0.0, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None],
             [2017, 2, 4, 1, 6, '2017-04-01', 'AA', 19805, 'AA', 'N798AA', 1,
              12478, 1247803, 31703, 'JFK', 'New York, NY', 'NY', 36,
              'New York', 22, 12892, 1289205, 32575, 'LAX', 'Los Angeles, CA',
              'CA', 6, 'California', 91, 800, 754.0, -6.0, 0.0, 0.0, -1.0,
              '0800-0859', 19.0, 813.0, 1046.0, 8.0, 1143, 1054.0, -49.0, 0.0,
              0.0, -2.0, '1100-1159', 0.0, None, 0.0, 403.0, 360.0, 333.0, 1.0,
              2475.0, 10, None, None, None, None, None, None, None, None, 0.0, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None],
             [2017, 2, 4, 30, 7, '2017-04-30', 'UA', 19977, 'UA', 'N66837', 10,
              12264, 1226402, 30852, 'IAD', 'Washington, DC', 'VA', 51,
              'Virginia', 38, 14747, 1474703, 30559, 'SEA', 'Seattle, WA',
              'WA', 53, 'Washington', 93, 1755, 1752.0, -3.0, 0.0, 0.0, -1.0,
              '1700-1759', 50.0, 1842.0, 2038.0, 6.0, 2049, 2044.0, -5.0, 0.0,
              0.0, -1.0, '2000-2059', 0.0, None, 0.0, 354.0, 352.0, 296.0, 1.0,
              2306.0, 10, None, None, None, None, None, None, None, None, 0.0, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None],
             [2017, 2, 4, 1, 6, '2017-04-01', 'B6', 20409, 'B6', 'N966JB', 1,
              12478, 1247803, 31703, 'JFK', 'New York, NY', 'NY', 36,
              'New York', 22, 11697, 1169704, 32467, 'FLL',
              'Fort Lauderdale, FL', 'FL', 12, 'Florida', 33, 1040, 1259.0,
              139.0, 139.0, 1.0, 9.0, '1000-1059', 24.0, 1323.0, 1542.0, 5.0,
              1345, 1547.0, 122.0, 122.0, 1.0, 8.0, '1300-1359', 0.0, None, 0.0,
              185.0, 168.0, 139.0, 1.0, 1069.0, 5, 9.0, 0.0, 0.0, 0.0, 113.0,
              None, None, None, 0.0, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None],
             [2017, 2, 4, 1, 6, '2017-04-01', 'WN', 19393, 'WN', 'N237WN',
              2366, 10140, 1014003, 30140, 'ABQ', 'Albuquerque, NM', 'NM', 35,
              'New Mexico', 86, 10821, 1082104, 30852, 'BWI', 'Baltimore, MD',
              'MD', 24, 'Maryland', 35, 550, 549.0, -1.0, 0.0, 0.0, -1.0,
              '0001-0559', 12.0, 601.0, 1120.0, 3.0, 1125, 1123.0, -2.0, 0.0,
              0.0, -1.0, '1100-1159', 0.0, None, 0.0, 215.0, 214.0, 199.0, 1.0,
              1670.0, 7, None, None, None, None, None, None, None, None, 0.0, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None],
             [2017, 2, 4, 22, 6, '2017-04-22', 'DL', 19790, 'DL', 'N938DL',
              2433, 10397, 1039705, 30397, 'ATL', 'Atlanta, GA', 'GA', 13,
              'Georgia', 34, 13495, 1349503, 33495, 'MSY', 'New Orleans, LA',
              'LA', 22, 'Louisiana', 72, 859, 855.0, -4.0, 0.0, 0.0, -1.0,
              '0800-0859', 19.0, 914.0, 918.0, 3.0, 927, 921.0, -6.0, 0.0, 0.0,
              -1.0, '0900-0959', 0.0, None, 0.0, 88.0, 86.0, 64.0, 1.0, 425.0,
              2, None, None, None, None, None, None, None, None, 0.0, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None]]

    input_cols = ['Year', 'Quarter', 'Month', 'DayofMonth', 'DayOfWeek', 'FlightDate', 
                  'Reporting_Airline', 'DOT_ID_Reporting_Airline', 'IATA_CODE_Reporting_Airline', 
                  'Tail_Number', 'Flight_Number_Reporting_Airline', 'OriginAirportID', 
                  'OriginAirportSeqID', 'OriginCityMarketID', 'Origin', 'OriginCityName', 
                  'OriginState', 'OriginStateFips', 'OriginStateName', 'OriginWac', 
                  'DestAirportID', 'DestAirportSeqID', 'DestCityMarketID', 'Dest', 'DestCityName', 
                  'DestState', 'DestStateFips', 'DestStateName', 'DestWac', 'CRSDepTime', 'DepTime', 
                  'DepDelay', 'DepDelayMinutes', 'DepDel15', 'DepartureDelayGroups', 'DepTimeBlk', 
                  'TaxiOut', 'WheelsOff', 'WheelsOn', 'TaxiIn', 'CRSArrTime', 'ArrTime', 'ArrDelay', 
                  'ArrDelayMinutes', 'ArrDel15', 'ArrivalDelayGroups', 'ArrTimeBlk', 'Cancelled', 
                  'CancellationCode', 'Diverted', 'CRSElapsedTime', 'ActualElapsedTime', 'AirTime', 
                  'Flights', 'Distance', 'DistanceGroup', 'CarrierDelay', 'WeatherDelay', 'NASDelay', 
                  'SecurityDelay', 'LateAircraftDelay', 'FirstDepTime', 'TotalAddGTime', 'LongestAddGTime', 
                  'DivAirportLandings', 'DivReachedDest', 'DivActualElapsedTime', 'DivArrDelay', 'DivDistance', 
                  'Div1Airport', 'Div1AirportID', 'Div1AirportSeqID', 'Div1WheelsOn', 'Div1TotalGTime', 
                  'Div1LongestGTime', 'Div1WheelsOff', 'Div1TailNum', 'Div2Airport', 'Div2AirportID', 
                  'Div2AirportSeqID', 'Div2WheelsOn', 'Div2TotalGTime', 'Div2LongestGTime', 'Div2WheelsOff', 
                  'Div2TailNum', 'Div3Airport', 'Div3AirportID', 'Div3AirportSeqID', 'Div3WheelsOn', 
                  'Div3TotalGTime', 'Div3LongestGTime', 'Div3WheelsOff', 'Div3TailNum', 'Div4Airport', 
                  'Div4AirportID', 'Div4AirportSeqID', 'Div4WheelsOn', 'Div4TotalGTime', 'Div4LongestGTime', 
                  'Div4WheelsOff', 'Div4TailNum', 'Div5Airport', 'Div5AirportID', 'Div5AirportSeqID', 
                  'Div5WheelsOn', 'Div5TotalGTime', 'Div5LongestGTime', 'Div5WheelsOff', 'Div5TailNum', 
                  'Unnamed: 109']

    df_input = pd.DataFrame(inputs, columns = input_cols)

    actual = [['2017-04-01', 2017, 4, 1, 6, 'AA', 'JFK', 'LAX', 800, 1143,
                -49.0, 0.0, 0.0, 1.0],
               ['2017-04-30', 2017, 4, 30, 7, 'UA', 'IAD', 'SEA', 1755, 2049,
                -5.0, 0.0, 0.0, 1.0],
               ['2017-04-01', 2017, 4, 1, 6, 'B6', 'JFK', 'FLL', 1040, 1345,
                122.0, 0.0, 0.0, 1.0],
               ['2017-04-01', 2017, 4, 1, 6, 'WN', 'ABQ', 'BWI', 550, 1125, -2.0,
                0.0, 0.0, 1.0],
               ['2017-04-22', 2017, 4, 22, 6, 'DL', 'ATL', 'MSY', 859, 927, -6.0,
                0.0, 0.0, 1.0]]

    actual_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 'Reporting_Airline', 
                   'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 'ArrDelay', 'Cancelled', 
                   'Diverted', 'Flights']

    df_true = pd.DataFrame(actual, columns = actual_cols)

    variable = 'Reporting_Airline'
    airlines = ['AA', 'B6', 'DL', 'UA', 'WN']
    columns = ['FlightDate','Year','Month', 'DayofMonth', 'DayOfWeek','Reporting_Airline', 
                  'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime','ArrDelay', 'Cancelled', 'Diverted', 
                  'Flights']

    df_test = ld.load_flight_data(df_input, variable, airlines, columns)

    df_test = df_test.reset_index(drop=True)

    assert df_test.equals(df_true)


def load_flight_data_unhappy():
    inputs = [[2017, 2, 4, 1, 6, '2017-04-01', 'EV', 20366, 'EV', 'N907EV',
              2755, 10185, 1018502, 30185, 'AEX', 'Alexandria, LA', 'LA', 22,
              'Louisiana', 72, 11298, 1129804, 30194, 'DFW',
              'Dallas/Fort Worth, TX', 'TX', 48, 'Texas', 74, 1019, 1007.0,
              -12.0, 0.0, 0.0, -1.0, '1000-1059', 19.0, 1026.0, 1117.0, 9.0,
              1137, 1126.0, -11.0, 0.0, 0.0, -1.0, '1100-1159', 0.0, None, 0.0,
              78.0, 79.0, 51.0, 1.0, 285.0, 2, None, None, None, None, None, None,
              None, None, 0.0, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None],
             [2017, 2, 4, 1, 6, '2017-04-01', 'AA', 19805, 'AA', 'N798AA', 1,
              12478, 1247803, 31703, 'JFK', 'New York, NY', 'NY', 36,
              'New York', 22, 12892, 1289205, 32575, 'LAX', 'Los Angeles, CA',
              'CA', 6, 'California', 91, 800, 754.0, -6.0, 0.0, 0.0, -1.0,
              '0800-0859', 19.0, 813.0, 1046.0, 8.0, 1143, 1054.0, -49.0, 0.0,
              0.0, -2.0, '1100-1159', 0.0, None, 0.0, 403.0, 360.0, 333.0, 1.0,
              2475.0, 10, None, None, None, None, None, None, None, None, 0.0, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None],
             [2017, 2, 4, 30, 7, '2017-04-30', 'UA', 19977, 'UA', 'N66837', 10,
              12264, 1226402, 30852, 'IAD', 'Washington, DC', 'VA', 51,
              'Virginia', 38, 14747, 1474703, 30559, 'SEA', 'Seattle, WA',
              'WA', 53, 'Washington', 93, 1755, 1752.0, -3.0, 0.0, 0.0, -1.0,
              '1700-1759', 50.0, 1842.0, 2038.0, 6.0, 2049, 2044.0, -5.0, 0.0,
              0.0, -1.0, '2000-2059', 0.0, None, 0.0, 354.0, 352.0, 296.0, 1.0,
              2306.0, 10, None, None, None, None, None, None, None, None, 0.0, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None],
             [2017, 2, 4, 1, 6, '2017-04-01', 'B6', 20409, 'B6', 'N966JB', 1,
              12478, 1247803, 31703, 'JFK', 'New York, NY', 'NY', 36,
              'New York', 22, 11697, 1169704, 32467, 'FLL',
              'Fort Lauderdale, FL', 'FL', 12, 'Florida', 33, 1040, 1259.0,
              139.0, 139.0, 1.0, 9.0, '1000-1059', 24.0, 1323.0, 1542.0, 5.0,
              1345, 1547.0, 122.0, 122.0, 1.0, 8.0, '1300-1359', 0.0, None, 0.0,
              185.0, 168.0, 139.0, 1.0, 1069.0, 5, 9.0, 0.0, 0.0, 0.0, 113.0,
              None, None, None, 0.0, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None],
             [2017, 2, 4, 1, 6, '2017-04-01', 'WN', 19393, 'WN', 'N237WN',
              2366, 10140, 1014003, 30140, 'ABQ', 'Albuquerque, NM', 'NM', 35,
              'New Mexico', 86, 10821, 1082104, 30852, 'BWI', 'Baltimore, MD',
              'MD', 24, 'Maryland', 35, 550, 549.0, -1.0, 0.0, 0.0, -1.0,
              '0001-0559', 12.0, 601.0, 1120.0, 3.0, 1125, 1123.0, -2.0, 0.0,
              0.0, -1.0, '1100-1159', 0.0, None, 0.0, 215.0, 214.0, 199.0, 1.0,
              1670.0, 7, None, None, None, None, None, None, None, None, 0.0, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None],
             [2017, 2, 4, 22, 6, '2017-04-22', 'DL', 19790, 'DL', 'N938DL',
              2433, 10397, 1039705, 30397, 'ATL', 'Atlanta, GA', 'GA', 13,
              'Georgia', 34, 13495, 1349503, 33495, 'MSY', 'New Orleans, LA',
              'LA', 22, 'Louisiana', 72, 859, 855.0, -4.0, 0.0, 0.0, -1.0,
              '0800-0859', 19.0, 914.0, 918.0, 3.0, 927, 921.0, -6.0, 0.0, 0.0,
              -1.0, '0900-0959', 0.0, None, 0.0, 88.0, 86.0, 64.0, 1.0, 425.0,
              2, None, None, None, None, None, None, None, None, 0.0, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None, None, None, None, None, None, None, None, None, None, None,
              None, None, None]]

    input_cols = ['Year', 'Quarter', 'Month', 'DayofMonth', 'DayOfWeek', 'FlightDate', 
                  'Reporting_Airline', 'DOT_ID_Reporting_Airline', 'IATA_CODE_Reporting_Airline', 
                  'Tail_Number', 'Flight_Number_Reporting_Airline', 'OriginAirportID', 
                  'OriginAirportSeqID', 'OriginCityMarketID', 'Origin', 'OriginCityName', 
                  'OriginState', 'OriginStateFips', 'OriginStateName', 'OriginWac', 
                  'DestAirportID', 'DestAirportSeqID', 'DestCityMarketID', 'Dest', 'DestCityName', 
                  'DestState', 'DestStateFips', 'DestStateName', 'DestWac', 'CRSDepTime', 'DepTime', 
                  'DepDelay', 'DepDelayMinutes', 'DepDel15', 'DepartureDelayGroups', 'DepTimeBlk', 
                  'TaxiOut', 'WheelsOff', 'WheelsOn', 'TaxiIn', 'CRSArrTime', 'ArrTime', 'ArrDelay', 
                  'ArrDelayMinutes', 'ArrDel15', 'ArrivalDelayGroups', 'ArrTimeBlk', 'Cancelled', 
                  'CancellationCode', 'Diverted', 'CRSElapsedTime', 'ActualElapsedTime', 'AirTime', 
                  'Flights', 'Distance', 'DistanceGroup', 'CarrierDelay', 'WeatherDelay', 'NASDelay', 
                  'SecurityDelay', 'LateAircraftDelay', 'FirstDepTime', 'TotalAddGTime', 'LongestAddGTime', 
                  'DivAirportLandings', 'DivReachedDest', 'DivActualElapsedTime', 'DivArrDelay', 'DivDistance', 
                  'Div1Airport', 'Div1AirportID', 'Div1AirportSeqID', 'Div1WheelsOn', 'Div1TotalGTime', 
                  'Div1LongestGTime', 'Div1WheelsOff', 'Div1TailNum', 'Div2Airport', 'Div2AirportID', 
                  'Div2AirportSeqID', 'Div2WheelsOn', 'Div2TotalGTime', 'Div2LongestGTime', 'Div2WheelsOff', 
                  'Div2TailNum', 'Div3Airport', 'Div3AirportID', 'Div3AirportSeqID', 'Div3WheelsOn', 
                  'Div3TotalGTime', 'Div3LongestGTime', 'Div3WheelsOff', 'Div3TailNum', 'Div4Airport', 
                  'Div4AirportID', 'Div4AirportSeqID', 'Div4WheelsOn', 'Div4TotalGTime', 'Div4LongestGTime', 
                  'Div4WheelsOff', 'Div4TailNum', 'Div5Airport', 'Div5AirportID', 'Div5AirportSeqID', 
                  'Div5WheelsOn', 'Div5TotalGTime', 'Div5LongestGTime', 'Div5WheelsOff', 'Div5TailNum', 
                  'Unnamed: 109']

    df_input = pd.DataFrame(inputs, columns = input_cols)

    actual = [['2017-04-01', 2017, 4, 1, 6, 'EV', 'AEX', 'DFW', 1019, 1137,
                -11.0, 0.0, 0.0, 1.0],
               ['2017-04-01', 2017, 4, 1, 6, 'AA', 'JFK', 'LAX', 800, 1143,
                -49.0, 0.0, 0.0, 1.0],
               ['2017-04-30', 2017, 4, 30, 7, 'UA', 'IAD', 'SEA', 1755, 2049,
                -5.0, 0.0, 0.0, 1.0],
               ['2017-04-01', 2017, 4, 1, 6, 'B6', 'JFK', 'FLL', 1040, 1345,
                122.0, 0.0, 0.0, 1.0],
               ['2017-04-01', 2017, 4, 1, 6, 'WN', 'ABQ', 'BWI', 550, 1125, -2.0,
                0.0, 0.0, 1.0],
               ['2017-04-22', 2017, 4, 22, 6, 'DL', 'ATL', 'MSY', 859, 927, -6.0,
                0.0, 0.0, 1.0]]

    actual_cols = ['FlightDate', 'Year', 'Month', 'DayofMonth', 'DayOfWeek', 'Reporting_Airline', 
                   'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime', 'ArrDelay', 'Cancelled', 
                   'Diverted', 'Flights']

    df_true = pd.DataFrame(actual, columns = actual_cols)

    variable = 'Reporting_AirlineWRONG'
    airlines = ['AA', 'B6', 'DL', 'UA', 'WN']
    columns = ['FlightDate','Year','Month', 'DayofMonth', 'DayOfWeek','Reporting_Airline', 
                  'Origin', 'Dest', 'CRSDepTime', 'CRSArrTime','ArrDelay', 'Cancelled', 'Diverted', 
                  'Flights']

    df_test = ld.load_flight_data(df_input, variable, airlines, columns)

    df_test = df_test.reset_index(drop=True)

    assert df_test.equals(df_true)


def run_load_data_tests():
    logger.debug('Testing functions from load_data script')

    logger.debug('Testing happy path on load_flight_data')
    load_flight_data_happy()

    logger.debug('Testing unhappy path on load_flight_data')
    load_flight_data_unhappy()

    










