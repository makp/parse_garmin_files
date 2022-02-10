from lst_workout_between_dates import select_workouts_between_dates
from filter_workouts import filter_workouts_by_type
from calc_HR_zones import add_hr_zones


def calc_perc_per_zone(df):
    total_per_zone = df.loc[:, 'z1/z2':].sum()
    total_time = total_per_zone.sum()
    return total_per_zone/total_time


df = select_workouts_between_dates(31)

df_running = add_hr_zones(filter_workouts_by_type(df))
