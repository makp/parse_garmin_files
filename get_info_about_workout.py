import gpxpy
import pandas as pd


def path_to_gpx(path_to_tcx):
    return path_to_tcx.split('.')[0] + '.gpx'


def get_workout_info(path_to_tcx):
    path = path_to_gpx(path_to_tcx)
    with open(path) as f:
        gpx = gpxpy.parse(f)
    # assert len(gpx.tracks) == 1, "This gpx file has 1+ tracks!!"
    workout = gpx.tracks[0]
    n, t = workout.name, workout.type
    return n, t


# nms_base = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'
# def get_workout_type(filepath):
#     with open(filepath) as f:
#         tcx = ET.parse(f)
#     root = tcx.getroot()
#     nsp = nms_base + 'Activities'
#     out = root.find(nsp)[0].get('Sport')
#     return out


def get_info_from_files(pseries):
    lst = []
    for _ in pseries:
        lst.append(get_workout_info(_))
    return lst
