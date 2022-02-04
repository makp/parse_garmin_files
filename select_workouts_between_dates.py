"""Select workout files based on a custom date range."""


import pandas as pd
import dateutil
import datetime as dt
import re
import glob

lst_files = glob.glob('activities/*.tcx')


def get_date_from_filename(s):
    """Get date from filenames and covert it to local time.
    This function assumes Garmin uses the UTC time standard."""
    d_str = re.split('/|\\+', s)[1]
    utc = dateutil.parser.isoparse(d_str)
    utc_tz = dateutil.tz.tzutc()
    local_tz = dateutil.tz.tzlocal()
    utc = utc.replace(tzinfo=utc_tz)
    return utc.astimezone(local_tz).date()


def get_date_last_monday():
    """Return date object corresponding to last Monday.
    TODO: Get date from a particular weekday (not just Monday)."""
    today = dt.datetime.now()
    ind = today.weekday()
    t = today - dt.timedelta(days=ind)
    return t.date()


def get_date_n_days_ago(val):
    """Return date object for n days ago or last Monday."""
    if val == "Mon":
        out = get_date_last_monday()
    else:
        today = dt.datetime.now()
        diff = today - dt.timedelta(days=val)
        out = diff.date()
    return out


def select_workouts_between_dates(t0="Mon", t1=0):
    workout_dates = [get_date_from_filename(s) for s in lst_files]
    df_workouts = pd.DataFrame(zip(workout_dates, lst_files),
                               columns=['date', 'file'])
    tstart = get_date_last_monday()
    tend = get_date_n_days_ago(t1)
    df_selection = df_workouts.query('date >= @tstart and date <= @tend')
    return df_selection.sort_values(by=['date'])
