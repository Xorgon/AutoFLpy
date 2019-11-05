# -*- coding: utf-8 -*-
"""
Unit tests for the flight_log_code.py and the log_to_xls.py
codes. *** WORK IN PROGRESS ***
No tests are currently written for the GUI.

@author Adrian Weishaeupl (aw6g15@soton.ac.uk)
"""

from autoflpy import log_to_xls
import unittest
import xlrd
import os
import json


class Testlog_to_xls(unittest.TestCase):

    def setUp(self):
        # Create variables and assign directories before any test.
        base_path = os.getcwd() + os.sep + "tests" + os.sep + "test_files" + \
            os.sep
        # Tidies up the base path for python.
        self.base_path = base_path.replace(os.sep, "/")
        # Reads the test_input_file information
        with open((base_path + 'test_Input File.json')) as file:
            self.data = json.load(file)
        # Sets dummy variables for testing to be used throughout.
        self.log_file_path = self.base_path + self.data["log_to_xls_input"][
                "log_file_path"] + self.data["log_to_xls_input"][
                "log_file_name"]
        self.name_converter_file_path = self.base_path + self.data[
                "log_to_xls_input"]["name_converter_file_path"]
        self.data_sources_path = self.base_path + self.data[
                "log_to_xls_input"]["data_sources_file_path"]
        self.excel_file_path = self.base_path
        self.excel_file_name = "test_xls"
        self.flight_date = self.data["log_to_xls_input"]["date"]
        self.flight_number = self.data["log_to_xls_input"]["flight_number"]

#    def tearDown(self):
#        # Remove variables and any files generated throughout the tests at the
#        # end of all tests.
#        pass

#    def test_log_to_xls_converter_interface(self):
#        # Need to find a way to test the internally defined functions.
#        # Need to find a way to test a GUI using unit tests.
#        pass

    def test_log_reader(self):
        # Make sure the test workbook is closed.
        log_to_xls.log_reader(self.log_file_path,
                              self.name_converter_file_path,
                              self.data_sources_path,
                              self.excel_file_path,
                              self.excel_file_name,
                              self.flight_date,
                              self.flight_number)

        def worksheet_tester(sheet, cell, expected_answer):
            """
            A function to check the values of specified cells in a workbook.
            """
            # Opens workbook created from test log file.
            test_workbook = xlrd.open_workbook(self.base_path +
                                               "/test_xls.xls")
            # Find the RCIN sheet and a cell (chosen to be mid flight).
            test_worksheet = test_workbook.sheet_by_name(sheet)
            # Checks a cell in the time column (unique).
            test_cell = test_worksheet.cell(cell[0], cell[1])
            self.assertEqual(str(test_cell.value), str(expected_answer))

        sheetlist = ["GPS", "RCIN", "BARO", "ARSP", "ATT", "VIBE", "CTUN",
                     "AOA"]
        # These values need to be adjusted if the
        # test_log_to_xls.log file gets changed.
        cell = [[699, 12], [3499, 14], [1399, 7], [1449, 8], [3499, 8],
                [3499, 6], [3499, 8], [3499, 2]]
        expected_answer = [210400613, 210661078, 210379062, 215459079,
                           210660279, 210661130, 210661044, 210661024]
        """
        The following loop checks that a value in each .xls sheet is correct.
        The chosen values are time values and hence there should only be one
        present per sheet.
        """
        for sheet in range(len(sheetlist)):
            worksheet_tester(sheetlist[sheet], cell[sheet],
                             expected_answer[sheet])


if __name__ == '__main__':
    unittest.main()