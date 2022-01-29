import gpxpy
import pandas as pd

with open("teste.gpx") as f:
    gpx = gpxpy.parse(f)

# Hierarchy Garmin gpx files:
# =gpx= -> =trk= (track/activity) -> =trkseg= ->
# -> =trkpt= (track points) -> =extensions=

assert len(gpx.tracks) == 1, "This gpx file has 1+ tracks!!"

activity = gpx.tracks[0]

# Get general info about activity
activity_name = activity.name
activity_type = activity.type
# activity_duration = activity.get_duration()

# Extract data points
datapoints = gpx.get_points_data()


def get_time_datapoint(p):
    return p.point.time


def get_time_increments(lst):
    new_lst = [0]
    for i in range(1, len(lst)):
        diff = lst[i] - lst[i-1]
        new_lst.append(diff.total_seconds())
    return new_lst


def get_hr_datapoint(p):
    assert len(p.point.extensions) == 1, "Datapoint contains 1+ extensions!!"
    elem = p.point.extensions[0]
    nsp_base = "{" + list(elem.nsmap.values())[0] + "}"
    nsp_hr = nsp_base + 'hr'
    ext_hr = elem.find(nsp_hr)
    try:
        hr = int(ext_hr.text)
    except AttributeError:
        hr = None
    return hr


ts = list(map(get_time_datapoint, datapoints))
delta = get_time_increments(ts)
hrs = list(map(get_hr_datapoint, datapoints))

df = pd.DataFrame(zip(delta, hrs), columns=['Secs', 'HRs'])
