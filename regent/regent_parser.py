# -*- coding:utf-8 -*-
from pprint import pprint
import xlrd


# 0.  '',
# 1.  Название (title)
# 2.  группа (type)
# 3.  артикул
# 4.  плотность, г/м² (density)
# 5.  ширина (height)
# 6.  длина (width)
# 7.  характеристика покрытия (surface)
# 8.  прайс лист за кг (ед отчета), руб.
# 9.  прайс лист за 1000 листов (ед склада), руб.
# 10. цена предложения  за кг (ед отчета), руб.
# 11. цена предложения за 1000 листов (ед склада), руб. (cost_thousand)

def parser(path_to_file):
    rb = xlrd.open_workbook(path_to_file)
    sheet = rb.sheet_by_index(0)
    data = []
    for row_num in xrange(min(10000, sheet.nrows)):
        row = sheet.row_values(row_num)
        if row[1] == u'' or row[1] == u'Название':
            continue

        sides = 0
        if row[2].find(u'Мелованная бумага') != -1:
            m_type = u'paper'
        elif row[2].find(u'') != -1:
            m_type = u'carton'
            sides = 1
        elif row[2].find(u'Первичный упаковочный') != -1:
            m_type = u'carton'
            sides = 2
        else:
            m_type = 'None'
        data.append({
            'type': m_type,
            'sides': sides,

            'title': row[1],
            'width': row[6],
            'height': row[5],
            'density': row[4],
            'surface': row[7],
            'cost_thousand': row[11],
            'machine_type': 'universal'
        })
    for d in data:
        print d['type'], d['sides'], d['title'], d['width'], d['height'], d['density'], d['surface'], d['cost_thousand'], d['machine_type']


parser('/home/crazyministr/work/providers_parsers/regent/v8_AE84_39.XLS.xlsx')
