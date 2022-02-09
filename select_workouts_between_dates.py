"""Select workout files based on a custom date range."""

import pandas as pd
import datetime as dt



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


def select_workouts_between_dates(df, t0="Mon", t1=0):
    tstart, tend = [get_date_n_days_ago(d) for d in [t0, t1]]
    df.query('date >= @tstart and date <= @tend', inplace=True)
    df.sort_values(by=['date'], inplace=True)
    return df.reset_index(drop=True)
