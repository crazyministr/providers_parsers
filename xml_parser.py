# -*- coding: utf-8 -*-
from pprint import pprint
import xml.etree.ElementTree as ET


def xml_parser(path_to_file):
    tree = ET.parse(path_to_file)
    root = tree.getroot()
    for group in root.findall('group'):
        print group.attrib['rus']  # type (мелованная бумага)
        data = []
        for papers in group.findall('papers'):
            print papers.attrib['rus']  # name (Джи-принт)
            materials = []  # all materials for current type
            for paper in papers.findall('paper'):
                fields = paper.find('fields')
                m = {'name': papers.attrib['eng']}
                for field in fields.findall('field'):
                    if field.get('name') == 'format':
                        m_format = field.text.split('*')
                        m['width'] = m_format[0]
                        m['height'] = m_format[1]
                    if field.get('name') == 'pl':
                        m['density'] = field.text
                materials.append(m)
            pprint(materials)
            data.append(materials)
        break

xml_parser('bereg-price.xml')
