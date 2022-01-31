import xml.etree.ElementTree as ET
import datetime as dt
import pandas as pd


nms_base = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'


def get_time_from_trackpoint(p):
    elem = p.find(nms_base + 'Time')
    return elem.text


def get_track_timestamps(track):
    lst = []
    for p in track:
        s1 = get_time_from_trackpoint(p)
        s2 = s1.split('T')[-1].split('.')[0]
        t = dt.datetime.strptime(s2, '%H:%M:%S')
        lst.append(t)
    return lst


def calc_increments(lst):
    new_lst = [0]
    for i in range(1, len(lst)):
        diff = lst[i] - lst[i-1]
        new_lst.append(diff.total_seconds())
    return new_lst


def calc_time_increments(tracks):
    """ Calculates the elapsed time between HR readings.
    BUG: This function produces negative values. This seems
    to occur when an HR reading occurs at midnight ('00:00:00').
    """
    out = []
    for track in tracks:
        lst = get_track_timestamps(track)
        lst_inc = calc_increments(lst)
        out.extend(lst_inc)
    return out


def get_hr_from_trackpoint(p):
    """Get HR from a Trackpoint field."""
    elem = p.find(nms_base + 'HeartRateBpm')
    try:
        hr = int(elem.find(nms_base + 'Value').text)
    except AttributeError:
        hr = None
    return hr


def create_pandas_with_hrs(filename):
    """Use the TCX file to create a Pandas dataframe with HRs.
TCX file hieararchy:
Root -> Activities -> Activity -> Lap -> Track -> Trackpoint"""
    filepath = "activities/" + filename + ".tcx"
    with open(filepath) as f:
        tcx = ET.parse(f)
    root = tcx.getroot()
    tracks = list(root.iter(nms_base + 'Track'))
    trackpoints = list(root.iter(nms_base + 'Trackpoint'))
    HRs = list(map(get_hr_from_trackpoint, trackpoints))
    deltas = calc_time_increments(tracks)
    df = pd.DataFrame(zip(deltas, HRs), columns=['Secs', 'HRs'])
    return df
