import xml.etree.ElementTree as ET
import datetime as dt
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
        s = get_time_from_trackpoint(d[i])
        s2 = s.split('T')[-1].split('.')[0]
        t = dt.datetime.strptime(s2, '%H:%M:%S')
        lst.append(t)
    return lst


def get_time_increments(lst):
    new_lst = [0]
    for i in range(1, len(lst)):
        diff = lst[i] - lst[i-1]
        new_lst.append(diff.total_seconds())
    return new_lst
