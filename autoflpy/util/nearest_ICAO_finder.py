# -*- coding: utf-8 -*-
"""
Finds the nearest ICAO from the generated data.

@author: Adrian Weishaeupl
aw6g15@soton.ac.uk 2019

runways.csv downloaded from https://github.com/sobester/ADRpy/blob/master/ADRpy
/data/runways.csv

NOTE: Finding runways.csv is a problem in the unit tests.
"""

import numpy as np
import os
import pandas as pd
import xlrd


def icao_finder(file_path, file_name):
    """Puts together sub-functions to find the UAV's nearest ICAO"""
    # Finds airport latitudes and longitudes
    airport_data = airport_lat_long()
    # Finds uav latitude and longitude at switch on
    uav_location = uav_lat_long(file_path, file_name)
    # Finds the ICAO code of the closest airfield
    nearest_icao = closest_icao(uav_location, np.array([airport_data[:, 1],
                                                       airport_data[:, 2]]))
    icao = airport_data[nearest_icao, 0]
    print(' Nearest ICAO = ' + str(icao))
    return(icao)


def closest_icao(UAV_lat_long, airport_lat_long):
    # Finds the closest airport to the latitudes and longitude of the UAV's
    # start location.
    # NOTE: selected airport may not have reliable METAR information.
    # based on code from: https://codereview.stackexchange.com/questions/28207/
    # finding-the-closest-point-to-a-list-of-points
    # Turns the airport list into a numpy array.
    airport_lat_long = np.asarray(airport_lat_long)
    # Finds the square distance to the closest airport - this is in terms of
    # difference in latitude and longitude (always positive).
    print('Calculating closest distance')
    dist_2 = np.sum((np.subtract(airport_lat_long, UAV_lat_long))**2, axis=0)
    if np.min(dist_2) > 0.05:
        print('Nearest airport weather data is not reliable')
    # Returns the array index of the closest airport
    return np.argmin(dist_2)


def airport_lat_long():
    """Returns a list of airport Latitudes and longitudes from runways.csv"""
    # Creates the file path and names the csv.
    print('Importing runway data. Adapted from: '
          'https://github.com/sobester/ADRpy')
    # Runways data is taken from ADRpy and has empty location cells filled with
    # very large numbers to eliminate the likelyhood of them being picked.
    file_path = os.path.join(os.path.dirname(__file__)[:-5], "data",
                             "runways.csv")
    # Creates pandas data frames for the data required.
    data = pd.read_csv(file_path)
    information = np.array([data['airport_ident'], data['le_latitude_deg'],
                            data['le_longitude_deg']])
    return(np.transpose(information))


def uav_lat_long(file_path, file_name):
    """Returns the UAV's latitude and longitude from the start of the flight
    (from the log files)"""
    # Reads from the xls document
    print('Finding UAV position')
    uav_log_file = xlrd.open_workbook(file_path + file_name)
    # Finds the GPS spreadsheet
    sheet = uav_log_file.sheet_by_name('GPS')
    # Finds the first entry for the latitude and longitude
    # NOTE: this might be unreliable for different input formats.
    uav_lat = float(sheet.cell(1, 5).value)
    uav_long = float(sheet.cell(1, 6).value)
    uav_position = np.array([[uav_lat], [uav_long]])
    print('UAV position = ' + str(uav_position))
    return uav_position