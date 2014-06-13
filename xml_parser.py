# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from pprint import pprint

indent = '    '

tree = ET.parse('bereg-price.xml')
root = tree.getroot()

for group in root.findall('group'):
    print group.attrib['rus']
    for papers in group.findall('papers'):
        print indent, papers.attrib['rus']
        for paper in papers.findall('paper'):
            f = []
            fields = paper.find('fields')
            for field in fields.findall('field'):
                f.append({
                    'name': field.get('name'),
                    'caption': field.get('caption'),
                    'value': field.text
                })
            print indent * 2, f
    break
