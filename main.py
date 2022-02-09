from lst_workout_between_dates import select_workouts_between_dates
from filter_workouts import filter_workouts_by_type
from calc_HR_zones import add_time_zones


df = select_workouts_between_dates(14)
df_running = add_time_zones(filter_workouts_by_type(df))
