import datetime
import xlrd


class ExcelReader:

    # default col
    col_map = {"time": 0, "city_code": 1, "city_name": 2,
               "AQI": 3, "PM2.5": 4, "PM10": 5,
               "SO2": 6, "NO2": 7, "O3": 8, "CO": 9}

    # default col to read 除AQI外的空气质量有关参数
    col_to_read = [4, 5, 6, 7, 8, 9]

    def __init__(self, path):
        self.file_path = path
        self.excel = xlrd.open_workbook(self.file_path)
        self.sheet = self.excel.sheet_by_index(0)  # read sheet (only 1)
        self.row = self.sheet.nrows  # read number of row
        self.col = self.sheet.ncols  # read number of col
        print(self.col_map)

    # 用于将单元格的格式进行转换
    def convert_cell_type(self, _cell):
        # 单元格的ctype属性为0时，对应的python格式为空字符串：''
        if _cell.ctype == 0:
            return 0

        # 单元格的ctype属性为2时，对应的python格式为float和int 将int分离出来
        elif _cell.ctype == 2 and _cell.value % 1 == 0.0:
            return int(_cell.value)

        # 单元格的ctype属性为3时，对应的python格式为datetime
        elif _cell.ctype == 3:
            return datetime.datetime(*xlrd.xldate_as_tuple(_cell.value, 0))

        # 单元格的ctype属性为4时，对应的python格式为Bool
        elif _cell.ctype == 4:
            return True if _cell.value == 1 else False

        # 单元格的ctype属性为1时，对应的python格式为字符串 默认返回字符串和ctype=2时的float类型的内容
        else:
            return _cell.value

    def read_by_city_name(self, city_name):
        city_name_row = self.sheet.col_values(self.col_map["city_name"])

        if bool(1 - city_name_row.__contains__(city_name)):
            return
        # the index of row which the city first appear
        first_index = city_name_row.index(city_name)

        city_name_row.reverse()
        # the index of row which the city last appear
        last_index = city_name_row.__len__() - 1 - city_name_row.index(city_name)

        result = []

        for i in range(first_index, last_index + 1):
            result_row = []
            for j in self.col_to_read:
                result_row.append(self.convert_cell_type(self.sheet.cell(i, j)))
            result.append(result_row)

        return result

    def read_by_city_code(self, city_code):
        city_code_row = self.sheet.col_values(self.col_map["city_code"])

        if bool(1 - city_code_row.__contains__(city_code)):
            return
        # the index of row which the city first appear
        first_index = city_code_row.index(city_code)

        city_code_row.reverse()
        # the index of row which the city last appear
        last_index = city_code_row.__len__() - 1 - city_code_row.index(city_code)

        result = []

        for i in range(first_index, last_index + 1):
            result_row = []
            for j in self.col_to_read:
                result_row.append(self.convert_cell_type(self.sheet.cell(i, j)))
            result.append(result_row)

        return result

    def read_all_col_to_read(self):
        result = []

        for i in range(1, self.row):
            result_row = []
            for j in self.col_to_read:
                result_row.append(self.convert_cell_type(self.sheet.cell(i, j)))
            result.append(result_row)

        return result

    def read_city_name_list(self):
        r = []

        for i in range(1, self.row):
            result_row = [self.convert_cell_type(self.sheet.cell(i, self.col_map['city_name']))]
            r.append(result_row)

        result = []
        for e in r:
            if e not in result:
                result.append(e)

        return result
