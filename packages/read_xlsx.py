# Dawei Li, 001022014

import xlrd


class XlsxReader(object):
    def __init__(self, file_loc):
        self.file_loc = file_loc
        self.data_sheet = None

    def read_data_sheet(self, sheet_num=0):
        """Read data from an excel sheet."""
        workbook = xlrd.open_workbook(self.file_loc)
        return workbook.sheet_by_index(sheet_num)
