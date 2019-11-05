# -*- coding: utf-8 -*-
"""
Unit tests for the flight_log_code.py and the log_to_xls.py
codes. *** WORK IN PROGRESS ***
No tests are currently written for the GUI.

@author Adrian Weishaeupl (aw6g15@soton.ac.uk)
"""

import unittest
import os
import json
import time
from autoflpy import flight_log_code
from datetime import datetime


class Test_flight_log_code(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        # Removes generated flight log.
        base_path = os.getcwd() + os.sep + "tests" + os.sep + \
                    "test_files" + os.sep
        os.remove(base_path + "test_generated_flight_log20190123 2.ipynb")

    def setUp(self):
        # Sets up all of the test variables and locations to be used
        # throughout.
        self.base_path = os.getcwd() + os.sep + "tests" + os.sep + \
                            "test_files" + os.sep
        self.base_path = self.base_path.replace(os.sep, "/")
        # Imports data from template.
        with open(self.base_path + 'test_Input File.json') as file:
            self.data = json.load(file)
        self.flight_number = self.data["log_to_xls_input"]["flight_number"]
        self.flight_date = self.data["log_to_xls_input"]["date"]
        self.template_file_path = self.base_path
        self.template_file_name = self.data["flight_log_generator_input"][
                "template_file_path"]
        self.flight_log_file_path = self.base_path + self.data[
                "flight_log_generator_input"]["flight_log_destination"]
        # NOTE: Need to find out what this is.
        self.flight_data_file_path = self.base_path
        self.flight_data_file_name = "test_xls.xls"
        self.arduino_flight_data_file_path = self.base_path + self.data[
                "flight_log_generator_input"]["arduino_flight_data_file_path"]
        self.arduino_flight_data_name = self.data["flight_log_generator_input"
                                                  ]["arduino_flight_data_name"]
        self.flight_log_file_name_header = "test_generated_flight_log"
        self.checklist_file_path = self.base_path
        self.log_code_version = "autoflpy.flight_log_code"
        self.ICAO_airfield = self.data["flight_log_generator_input"][
                "icao_code"]
        self.start_time_hours = self.data["flight_log_generator_input"][
                "start_time_hours"]
        self.end_time_hours = self.data["flight_log_generator_input"][
                "end_time_hours"]
        self.metar_file_path = self.base_path + self.data[
                "flight_log_generator_input"]["metar_file_path"]

    def test_flight_log_maker(self):
        flight_log_code.flight_log_maker(self.template_file_path,
                                         self.template_file_name,
                                         self.flight_log_file_path,
                                         self.flight_data_file_path,
                                         self.flight_data_file_name,
                                         self.arduino_flight_data_file_path,
                                         self.arduino_flight_data_name,
                                         self.flight_date,
                                         self.flight_number,
                                         self.flight_log_file_name_header,
                                         self.checklist_file_path,
                                         self.log_code_version,
                                         self.ICAO_airfield,
                                         self.start_time_hours,
                                         self.end_time_hours,
                                         self.metar_file_path)
        # This code tests the flight_log_maker function.
        # First, check that a file has been created.
        test_flight_log_file_path = self.base_path + \
            'test_generated_flight_log20190123 2.ipynb'
        if os.path.exists(test_flight_log_file_path) is True:
            file_exists = True
        self.assertTrue(file_exists)
        # Checks that the file was recently created.
        filetime = os.stat(test_flight_log_file_path)
        # Finds the time since the file has been created.
        time_diff = datetime.now() - datetime.fromtimestamp(filetime.st_mtime)
        # Checks that the time difference is less than 1 second.
        self.assertLess(time_diff.microseconds, 1e6)
        # Check that the files weren't created in the past.
        self.assertGreater(time_diff.microseconds, 0)

    def test_flight_data(self):
        # Tests the flight data code.
        frame_list = flight_log_code.flight_data(
                self.flight_data_file_path,
                self.flight_data_file_name)
        # Checks that the expected frame dimensions are the correct size.
        frame_dimensions = [17693, 102030, 21784, 24498, 61218, 47614, 61218,
                            20406]
        if len(frame_list) == 8:
            for frame in range(len(frame_list)):
                self.assertEqual(frame_list[frame].size,
                                 frame_dimensions[frame])
        else:
            # Raises a fault if the length of the frame_list is not as
            # expected.
            self.assertEqual(1, 2)

    def test_checklist_finder(self):
        pass


if __name__ == '__main__':
    unittest.main()