import pandas as pd
from select_workouts_between_dates import select_workouts_between_dates
from get_info_about_workout import get_info_from_files


df1 = select_workouts_between_dates()
df1.reset_index(drop=True, inplace=True)
df2 = get_info_from_files(df1.loc[:, 'file'])
df3 = pd.concat([df1, df2], axis=1)
df3.drop('file', axis=1, inplace=True)
df3.query("type == 'treadmill_running' or type == 'running'")
