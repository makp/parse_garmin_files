import gpxpy
import pandas as pd


def path_to_gpx(path_to_tcx):
    return path_to_tcx.split('.')[0] + '.gpx'


def get_workout_info(path_to_tcx):
    """Get name and type of a workout from its gpx file."""
    path = path_to_gpx(path_to_tcx)
    with open(path) as f:
        gpx = gpxpy.parse(f)
    # assert len(gpx.tracks) == 1, "This gpx file has 1+ tracks!!"
    workout = gpx.tracks[0]
    n, t = workout.name, workout.type
    d = workout.description
    return n, t, d


# nms_base = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'
# def get_workout_type(filepath):
#     with open(filepath) as f:
#         tcx = ET.parse(f)
#     root = tcx.getroot()
#     nsp = nms_base + 'Activities'
#     out = root.find(nsp)[0].get('Sport')
#     return out


def get_info_from_files(pseries):
    """Return a Pandas dataframe with name and type of each workout."""
    dic = {'name': [], 'type': [], 'desc': []}
    for _ in pseries:
        n, t, d = get_workout_info(_)
        dic['name'].append(n)
        dic['type'].append(t)
        dic['desc'].append(d)
    return pd.DataFrame(dic)
