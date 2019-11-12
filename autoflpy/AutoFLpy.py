"""
This modules allows for the running of the log to xls converter and the
automatic flight log generator.
"""

__author__ = "Adrian Weishaeupl"

import autoflpy.util.name_generator as name_generator
import os
import json
import autoflpy.util.flight_log_code as flight_log_code
import autoflpy.util.log_to_xls as log_to_xls
import autoflpy.util.nearest_ICAO_finder as nearest_ICAO_finder
from shutil import copyfile

"""
TODO:
    Finish writing unittests.
    Find why the METAR information displays the incorrect date/data.
    Remove the code from the Jupyter template and move it out of sight.
    Find a way that the code can recognise if the nearest airfield has weather
        data.
    Find a way of allowing custom weather data to be added - add it into the
        input file.
    Fix checklist integration into notebook.
    Examples in the example folder.
    Make the code access the template from the current working directory or the
        default directory.
    Make it easier to find the sample data (arduino and xls).
    Allow for channel mapping in the flight log code.
    Throttle as a %??
    Place the input file into the current directory.
"""


def autoflpy(input_file='Input File.json'):
    # Finds the file path from where this code is being run.
    base_path = os.path.join(os.path.dirname(__file__), "data") + os.sep
    # Tidies up the base path for python.
    base_path = base_path.replace(os.sep, "/")

    # Sets the default storage location in the working directory.
    default_storage_path = str((os.getcwd() + os.sep + 'user_files' + os.sep
                                ).replace(os.sep, "/"))

    # Copies the standard input file into the working directory
    if os.path.exists(default_storage_path + input_file) is False:
        copyfile(base_path + input_file, default_storage_path + input_file)
    else:
        pass

    # Copies the template input file into the current working directory
    input_template_file = 'Input Template.json'
    if os.path.exists(default_storage_path + input_template_file) is False:
        copyfile(base_path + input_template_file, default_storage_path +
                 input_template_file)
    else:
        pass

    # Reads the test_input_file information.
    with open(default_storage_path + input_file) as file:
        data = json.load(file)

    # Sets  variables from the input file to be used.
    # If no log file path has been entered, go to the standard log path.
    if data["log_to_xls_input"]["log_file_path"] != "" and os.path.exists(
            data["log_to_xls_input"]["log_file_path"]) is True:
        log_file_path = (data["log_to_xls_input"][
            "log_file_path"] + os.sep + data["log_to_xls_input"][
            "log_file_name"]).replace(os.sep, "/")
    else:
        # Creates a new directory to look for files.
        log_file_base_path = default_storage_path + "log_files"
        log_file_path = (log_file_base_path + os.sep + data[
                "log_to_xls_input"]["log_file_name"]).replace(os.sep, "/")
        try:
            os.makedirs(log_file_base_path)
            # Raises error and gives advice on how to continue.
            print('No log file directory was entered. A new directory has been\
              made, please copy the file path of this directory into the \
              input file and place your log files into this directory.')
            raise FileNotFoundError
        except OSError:
            print('Log file path found.')
    name_converter_file_path = base_path + 'Name converter list.txt'
    data_sources_path = base_path + 'Data sources.txt'
    # If no excel data file path has been entered, go to the standard path.
    if data["log_to_xls_input"]["excel_data_file_path"] != "" and \
        os.path.exists(
            data["log_to_xls_input"]["excel_data_file_path"]) is True:
        excel_file_path = (data["log_to_xls_input"][
            "excel_data_file_path"]).replace(os.sep, "/")
    else:
        # Makes a directory in the current working path to be used.
        excel_file_path = default_storage_path + "excel_file_path"
        try:
            os.makedirs(excel_file_path)
        except OSError:
            print('Excel folder found. Will use this folder to store generated\
                  xls files.')

    flight_date = data["log_to_xls_input"]["date"]
    flight_number = data["log_to_xls_input"]["flight_number"]
    name_generator.excel_file_name_updater(flight_date, flight_number)
    # Generates an appropriate file name
    excel_file_name = name_generator.generated_file_name

    # Runs the xls converter
    log_to_xls.log_reader(log_file_path,
                          name_converter_file_path,
                          data_sources_path,
                          excel_file_path,
                          excel_file_name,
                          flight_date,
                          flight_number)

    # Assigns variables - checks if any information is entered into the input
    # file for the directories before creating new directories in the current
    # working directory.
    if data["flight_log_generator_input"]["template_file_path"] != "" and \
        os.path.exists(
            data["flight_log_generator_input"]["template_file_path"]) is True:
        template_file_path = (data["flight_log_generator_input"][
            "template_file_path"]).replace(os.sep, "/")
    else:
        template_file_path = base_path
    if data["flight_log_generator_input"]["template_file_name"] != "" and \
        os.path.exists(
            data["flight_log_generator_input"]["template_file_name"]) is True:
        template_file_name = data["flight_log_generator_input"][
            "template_file_name"]
    else:
        template_file_name = 'Default Template (Full Summary).ipynb'
    if data["flight_log_generator_input"]["flight_log_destination"] != "" and \
        os.path.exists(
            data["flight_log_generator_input"][
                    "flight_log_destination"]) is True:
        flight_log_file_path = data["flight_log_generator_input"][
                "flight_log_destination"]
    else:
        # Makes a directory in the current working path to be used.
        flight_log_file_path = default_storage_path + "flight_logs_generated"
        try:
            os.makedirs(flight_log_file_path)
        except OSError:
            print('Flight log folder found. Will use this folder to store\
                  generated flight log files.')
    flight_data_file_path = (excel_file_path + os.sep).replace(os.sep, "/")
    flight_data_file_name = excel_file_name + ".xls"
    if data["flight_log_generator_input"][
            "arduino_flight_data_file_path"] != "" and \
        os.path.exists(data["flight_log_generator_input"]
                       ["arduino_flight_data_file_path"]) is True:
        arduino_flight_data_file_path = data[
            "flight_log_generator_input"]["arduino_flight_data_file_path"]
    else:
        # Makes a directory in the current working path to be used.
        arduino_flight_data_file_path = default_storage_path + \
            "arduino_flight_data"
        try:
            os.makedirs(arduino_flight_data_file_path)
        except OSError:
            print('Arduino flight data folder found.')
    arduino_flight_data_name = data["flight_log_generator_input"][
            "arduino_flight_data_name"]
    flight_log_file_name_header = "Generated flight log"
    if data["flight_log_generator_input"][
            "checklist_data_file_path"] != "" and \
        os.path.exists(data[
            "flight_log_generator_input"]["checklist_data_file_path"]) is True:
        checklist_file_path = data[
            "flight_log_generator_input"]["checklist_data_file_path"]
    else:
        # Makes a directory in the current working path to be used.
        checklist_file_path = default_storage_path + "checklists"
        try:
            os.makedirs(checklist_file_path)
        except OSError:
            print('Checklists folder found.')
    log_code_version = "autoflpy.util.flight_log_code"
    start_time_hours = data["flight_log_generator_input"]["start_time_hours"]
    end_time_hours = data["flight_log_generator_input"]["end_time_hours"]
    if data["flight_log_generator_input"][
            "metar_file_path"] != "" and \
        os.path.exists(
            data["flight_log_generator_input"]["metar_file_path"]) is True:
        metar_file_path = data[
            "flight_log_generator_input"]["metar_file_path"]
    else:
        # Makes a directory in the current working path to be used.
        metar_file_path = default_storage_path + "METAR_storage"
        try:
            os.makedirs(metar_file_path)
        except OSError:
            print('METAR storage folder found.')
    # Finds the nearest airfield for METAR information
    ICAO_airfield = nearest_ICAO_finder.icao_finder(flight_data_file_path,
                                                    flight_data_file_name)

    # Runs the flight log generator
    flight_log_code.flight_log_maker(template_file_path,
                                     template_file_name,
                                     flight_log_file_path,
                                     flight_data_file_path,
                                     flight_data_file_name,
                                     arduino_flight_data_file_path,
                                     arduino_flight_data_name,
                                     flight_date,
                                     flight_number,
                                     flight_log_file_name_header,
                                     checklist_file_path,
                                     log_code_version,
                                     ICAO_airfield,
                                     start_time_hours,
                                     end_time_hours,
                                     metar_file_path)


if __name__ == "__main__":
    autoflpy()
