import pandas as pd
from select_workouts_between_dates import select_workouts_between_dates
from get_info_about_workout import get_info_from_files
from calc_HR_zones import create_df_with_zones


def filter_workouts_by_date(df, t0="Mon", t1=0):
    """List workouts and their info within a time range."""
    df1 = select_workouts_between_dates(t0, t1)
    df2 = get_info_from_files(df1.loc[:, 'file'])
    return pd.concat([df1, df2], axis=1)


def filter_workouts_by_type(df, key='running'):
    """Filter workouts based on the type (e.g., running)."""
    if key == 'running':
        out = df.query("type == 'treadmill_running' or type == 'running'")
    out.reset_index(drop=True, inplace=True)
    return out


def add_time_zones(df):
    """Add columns with the time spent at each zone."""
    df_zones = create_df_with_zones(df['file'])
    out = pd.concat([df, df_zones], axis=1)
    out.loc[:, 'z1/z2':'z5'] = round(out.loc[:, 'z1/z2':'z5']/60, 1)
    return out
