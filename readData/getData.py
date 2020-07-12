from readData import reader
import shelve
import numpy
import torch


class GetData:

    def __init__(self):
        self.data = []  # 最后输出为(1812,367,6)
        self.data_isRead = False
        self.max = []
        self.min = []
        self.data_isNor = False

    def save_class(self):
        with shelve.open("readData/data_class.abc", 'n') as s:
            s['class'] = self

    @staticmethod
    def load_class():
        with shelve.open("readData/data_class.abc", 'r') as s:
            return s['class']

    def change_shape(self, data):
        data = numpy.reshape(data, (1, len(data) * 6))
        return data.tolist()[0]

    def read_data(self):

        if self.data_isRead:
            with shelve.open("readData/data.abc", flag='r') as s:
                self.data = s['data']

        else:
            data_reader_2015 = reader.ExcelReader("readData/ebd_city_2015_day.xlsx")
            data_reader_2016 = reader.ExcelReader("readData/ebd_city_2016_day.xlsx")
            data_reader_2017 = reader.ExcelReader("readData/ebd_city_2017_day.xlsx")
            data_reader_2018 = reader.ExcelReader("readData/ebd_city_2018_day.xlsx")
            data_reader_2019 = reader.ExcelReader("readData/ebd_city_2019_day.xlsx")
            cities = data_reader_2015.read_city_name_list()
            i = 0

            for city in cities:
                city_data = []
                y2015_data = data_reader_2015.read_by_city_name(city[0])
                y2015_data = self.change_shape(y2015_data)
                y2016_data = data_reader_2016.read_by_city_name(city[0])
                y2016_data = self.change_shape(y2016_data)
                y2017_data = data_reader_2017.read_by_city_name(city[0])
                y2017_data = self.change_shape(y2017_data)
                y2018_data = data_reader_2018.read_by_city_name(city[0])
                y2018_data = self.change_shape(y2018_data)
                y2019_data = data_reader_2019.read_by_city_name(city[0])
                y2019_data = self.change_shape(y2019_data)

                if city[0] == '莱芜':
                    city_data = y2015_data + y2016_data + y2017_data + y2018_data + y2019_data[0:257 * 6] \
                                + y2018_data[257 * 6:357 * 6]
                elif city[0] == '铜仁地区':
                    city_data = y2015_data + y2016_data + y2017_data + y2018_data + y2019_data[0:137 * 6] \
                                + y2018_data[137 * 6:357 * 6]
                else:
                    city_data = y2015_data + y2016_data + y2017_data + y2018_data + y2019_data[0:357 * 6]

                city_data = numpy.array(city_data, dtype=float)
                city_data.resize(1812, 1, 6)
                if i == 0:
                    self.data = city_data
                    i += 1
                else:
                    self.data = numpy.concatenate((self.data, city_data), axis=1)

            self.save_data()
            self.data_isRead = True
            # 15 self.change_shape(364, 367, 6)
            # 16 self.change_shape(366, 367, 6)
            # 17 self.change_shape(365, 367, 6)
            # 18 self.change_shape(360, 367, 6)
            # 19 self.change_shape(357 ?, 367, 6)

    def save_data(self):
        with shelve.open('readData/data.abc', flag='n') as s:
            s['data'] = self.data

    def normalization(self):
        if self.data_isNor:
            return
        self.read_data()
        for i in range(0, 6):
            data_column = []
            for x in range(0, 1812):
                for y in range(0, 367):
                    data_column.append(self.data[x][y][i])
            data_column = numpy.array(data_column, dtype=float)
            self.max.append(data_column.max())
            self.min.append(data_column.min())

            for a in range(0, len(data_column)):
                data_column[a] = (data_column[a] - self.min[i]) / (self.max[i] - self.min[i])
            index = 0
            for x in range(0, 1812):
                for y in range(0, 367):
                    self.data[x][y][i] = data_column[index]
                    index += 1
        self.data_isNor = True

    def renormalization(self, data_to_re, x, y, z):

        for i in range(0, x):
            for j in range(0, y):
                for k in range(0, z):
                    data_to_re[i][j][k] = data_to_re[i][j][k] * (self.max[k] - self.min[k]) + self.min[k]

        return data_to_re

    def get_nor_data(self):

        self.normalization()
        self.save_data()
        return torch.FloatTensor(self.data)

