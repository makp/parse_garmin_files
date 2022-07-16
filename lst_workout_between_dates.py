"""List Garmin .TCX files and general info based on a date range."""

import pandas as pd
import glob
import dateutil
import datetime as dt
import re


path_to_garmin_files = 'workouts/'


def get_date_from_filename(s):
    """Get date from filenames and covert it to local time. This
    function assumes that Garmin utilizes the UTC time standard."""
    d_str = re.split('/|\\+', s)[1]
    utc = dateutil.parser.isoparse(d_str)
    utc_tz = dateutil.tz.tzutc()
    local_tz = dateutil.tz.tzlocal()
    utc = utc.replace(tzinfo=utc_tz)
    return utc.astimezone(local_tz).date()


def create_df():
    """Return a Pandas Dataframe containing the path to every Garmin
    .TCX file and its date in the local time zone---instead of the UTC
    time standard."""
    lst_files = glob.glob(path_to_garmin_files + '*.tcx')
    lst_dates = [get_date_from_filename(f) for f in lst_files]
    df = pd.DataFrame(zip(lst_dates, lst_files),
                      columns=['date', 'file'])
    df.sort_values(by=['date'], inplace=True)
    return df.reset_index(drop=True)


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
    """Select workouts within a data range and get general info about
    workouts."""
    df = create_df()
    tstart, tend = [get_date_n_days_ago(d) for d in [t0, t1]]
    df.query('date >= @tstart and date <= @tend', inplace=True)
    df.sort_values(by=['date'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df
