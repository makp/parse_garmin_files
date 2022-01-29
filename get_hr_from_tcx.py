import xml.etree.ElementTree as ET
# import pandas as pd

with open("teste.tcx") as f:
    tcx = ET.parse(f)

# TCX file hieararchy:
# Root -> Activities -> Activity -> Lap -> Track -> Trackpoint


root = tcx.getroot()

nms_base = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'

datapoints = list(root.iter(nms_base + 'Trackpoint'))


def get_time_from_trackpoint(p):
    elem = p.find(nms_base + 'Time')
    return elem.text


def get_time_from_datapoints(d):
    lst = []
    for i in range(1, len(d)):
        t = get_time_from_trackpoint(d[i])
        lst.append(t)
    return lst
