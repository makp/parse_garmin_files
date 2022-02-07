import pandas as pd
from select_workouts_between_dates import select_workouts_between_dates
from get_info_about_workout import get_info_from_files
from calc_HR_zones import create_pandas_with_zones

#  TODO: Streamline code.

df1 = select_workouts_between_dates()
df2 = get_info_from_files(df1.loc[:, 'file'])
df3 = pd.concat([df1, df2], axis=1)
df3.query("type == 'treadmill_running' or type == 'running'", inplace=True)
df3.reset_index(drop=True, inplace=True)
df4 = create_pandas_with_zones(df3['file'])
df5 = pd.concat([df3, df4], axis=1)
df5.loc[:, 'z1/z2':'z5'] = round(df5.loc[:, 'z1/z2':'z5']/60, 1)
df5.drop('file', axis=1, inplace=True)
