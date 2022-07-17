"""Extract HRs from .TCX files and smooth HR values.

TCX file hieararchy:
Root -> Activities -> Activity -> Lap -> Track -> Trackpoint

Trackpoints are individual readings (HR, position, etc).

I suspect pauses occur when the time difference between Trackpoints
is higher than one second.
"""


import xml.etree.ElementTree as ET
import dateutil.parser
import numpy as np
import pandas as pd


nms_base = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'


def get_hr_from_trackpoint(p):
    """Get HR from a Trackpoint field."""
    elem = p.find(nms_base + 'HeartRateBpm')
    try:
        hr = int(elem.find(nms_base + 'Value').text)
    except AttributeError:
        hr = None
    return hr


def get_time_from_trackpoint(p):
    """Get UTC time from a Trackpoint."""
    elem = p.find(nms_base + 'Time')
    return elem.text


def parse_time_from_track(track):
    """List UTC time of each Trackpoint within a Track and parse it."""
    lst = []
    for p in track:
        s1 = get_time_from_trackpoint(p)
        t = dateutil.parser.isoparse(s1)
        lst.append(t)
    return lst


def calc_time_increments(lst):
    """Return list with time increments in seconds from a list of consecutive
    datetime objects."""
    new_lst = [1]
    for i in range(1, len(lst)):
        diff = lst[i] - lst[i-1]
        new_lst.append(diff.total_seconds())
    return new_lst


def calc_elapsed_time_between_trackpoints(tracks):
    """Calculate elapsed time between Trackpoints of a list of Tracks."""
    out = []
    for track in tracks:
        lst = parse_time_from_track(track)
        lst_inc = calc_time_increments(lst)
        out.extend(lst_inc)
    return out


def add_hr_values(arr1d):
    hr1, hr2, dt = arr1d
    s = int(dt) + 2
    out = np.ones((s, 2))
    extra_hrs = np.rint(np.linspace(hr1, hr2, s))
    out[:, 1] = extra_hrs
    return out


def hr_linearize(arr):
    out = [add_hr_values(e) for e in arr]
    return np.concatenate(out)


def smooth_HR_readings(df):
    """Smooth the recorded HR values."""
    df_1 = df[df['Secs'] == 1]
    mask_2 = df['Secs'] > 1     # problematic reading
    mask_1 = mask_2.shift(-1)   # previous reading
    mask_1.iloc[-1] = False     # otherwise the last element is a NaN value
    arr_hr1 = df[mask_1]['HRs'].values
    arr_hr2 = df[mask_2]['HRs'].values
    arr_dt = df[mask_2]['Secs'].values
    arr = np.array([arr_hr1, arr_hr2, arr_dt])
    df_2 = pd.DataFrame(hr_linearize(np.transpose(arr)),
                        columns=["Secs", "HRs"])
    return pd.concat([df_1, df_2], ignore_index=True)


def create_pandas_with_hrs(filepath):
    """Create a Pandas dataframe with HRs from a .TCX file and smooth
    the readings."""
    with open(filepath) as f:
        tcx = ET.parse(f)
    root = tcx.getroot()
    tracks = list(root.iter(nms_base + 'Track'))
    trackpoints = list(root.iter(nms_base + 'Trackpoint'))
    HRs = list(map(get_hr_from_trackpoint, trackpoints))
    deltas = calc_elapsed_time_between_trackpoints(tracks)
    df = pd.DataFrame(zip(deltas, HRs), columns=['Secs', 'HRs'])
    return smooth_HR_readings(df)['HRs']
