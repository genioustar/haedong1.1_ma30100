import xlrd
from define import *

wb = xlrd.open_workbook('C:\\Users\\porsche\\Desktop\\haedong1.1_waterfull\\haedong1.1\\day.xlsx')
sh = wb.sheet_by_index(0)

nrow = sh.nrows

data = []

for i in range(1, nrow):
    candle = {}
    candle[DATE] = sh.cell_value(i, 0)
    candle[OPEN] = sh.cell_value(i, 1)
    candle[HIGH] = sh.cell_value(i, 2)
    candle[LOW] = sh.cell_value(i, 3)
    candle[CLOSE] = sh.cell_value(i, 4)
    candle[VOLUME] = sh.cell_value(i, 5)
    data.append(candle)


def calc_ma_from_xls(type, length, date, current_price):
    i = 0
    print(date)
    print(data[i][DATE])
    for i in range(0, len(data)):
        if date.replace('-', '/') <= data[i][DATE]:
            break

    print(data[i])
    sum = 0
    for j in range(i-(length-1), i):
        sum = sum + data[j][CLOSE]

    sum = sum + current_price

    ma = float(sum) / float(length)

    print(ma)

calc_ma_from_xls(MA, 3, '2017-11-28', 1240.0)