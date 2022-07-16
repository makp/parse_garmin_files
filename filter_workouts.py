import pandas as pd

from lst_workout_between_dates import select_workouts_between_dates
from get_info_about_workout import get_info_from_files


def filter_workouts_by_type(df, key='running'):
    """Filter workouts based on whether they are cycling, running, or
    cardio activities."""
    cond_running = "type == 'treadmill_running' or type == 'running'"
    cond_cycling = "type == 'indoor_cycling' or type == 'cyclying'"
    cond_cardio = cond_running + " or " + cond_cycling
    if key == 'running':
        out = df.query(cond_running)
    elif key == 'cycling':
        out = df.query(cond_cycling)
    elif key == 'cardio':
        out = df.query(cond_cardio)
    out.reset_index(drop=True, inplace=True)
    return out


def filter_workouts_by_date_and_type(t0="Mon", t1=0, key='running'):
    """Filter workouts by date and type."""
    df1 = select_workouts_between_dates(t0, t1)
    df2 = get_info_from_files(df1.loc[:, 'file'])
    df_all = pd.concat([df1, df2], axis=1)
    out = filter_workouts_by_type(df_all, key)
    return out.drop(['file', 'type'], axis=1)
