# -*- coding: utf-8 -*-
from pprint import pprint
import urllib2
import xml.etree.ElementTree as ET

eur_rate = None
URL = "http://spb.bereg.net/price.xml"
FILE_TO_SAVE = "bereg-price.xml"
PARSE_PAPERS = [u'Мелованная бумага', u'Офсетная бумага']


def eur_to_rub(cost):
    if eur_rate is None:
        raise Exception("eur rate is None")
    return cost * eur_rate


def cost_1th_to_cost1000sheets(cost_1th, density, width, height):
    # width must be more than height
    """
        width and height converting to meters (default centimeter)
        cost for 1 gram = (cost for 1 ton) / 1000000
        cost for 1 sheet = (cost for 1 gram) * density * width * height
        result = (cost for 1 sheet) * 1000
    """
    width /= 100
    height /= 100
    return cost_1th / 1000000 * density * width * height * 1000


def xml_parser(path_to_file):
    print "parse xml..."
    global eur_rate

    tree = ET.parse(path_to_file)
    root = tree.getroot()
    eur_rate = float(root.get("eur"))
    data = []
    for group in root.findall('group'):
        # print group.attrib['rus']  # type (мелованная бумага)
        if not group.get('rus') in PARSE_PAPERS:
            continue
        for papers in group.findall('papers'):
            # print papers.get('rus')  # name (Джи-принт)
            materials = []  # all materials for current type
            for paper in papers.findall('paper'):
                fields = paper.find('fields')
                surface = papers.get('surface')
                m = {'name': papers.get('eng') or papers.get('rus'),
                     'surface': 'matted' if surface == 'matt'
                                else
                                'glossy' if surface == 'gloss'
                                else 'no',
                     'machine_type': 'universal',
                     'type': 'paper' if group.get('rus') == PARSE_PAPERS[0]
                             else
                             'offset' if group.get('rus') == PARSE_PAPERS[1]
                             else '',
                }
                for field in fields.findall('field'):
                    if field.get('name') == 'format':
                        m_format = field.text.split('*')
                        m['width'] = m_format[0]
                        m['height'] = m_format[1]
                    if field.get('name') == 'pl':
                        m['density'] = field.text
                    if field.get('name') == 'price':
                        m['cost'] = eur_to_rub(
                            cost_1th_to_cost1000sheets(
                                float(field.text),
                                float(paper.get('pl')),
                                float(paper.get('fl')),
                                float(paper.get('fw'))))
                materials.append(m)
            pprint(materials)
            data.append(materials)
    return data


def get_xml_by_url(url, file_to_save):
    print "fetch xml..."
    source = urllib2.urlopen(url)
    content = source.read()
    f = open(file_to_save, "w")
    f.write(content)
    f.close()


def get_bereg_data():
    global FILE_TO_SAVE
    get_xml_by_url(URL, FILE_TO_SAVE)
    return xml_parser(FILE_TO_SAVE)


pprint(get_bereg_data())
