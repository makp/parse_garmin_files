from get_hr_from_tcx import create_pandas_with_hrs
import pandas as pd
import dateutil
import datetime as dt
import re
import glob

lst_files = glob.glob('activities/*.tcx')


def get_date_from_filename(s):
    d_str = re.split('/|\\+', s)[1]
    utc = dateutil.parser.isoparse(d_str)
    utc_tz = dateutil.tz.tzutc()
    local_tz = dateutil.tz.tzlocal()
    utc = utc.replace(tzinfo=utc_tz)
    return utc.astimezone(local_tz).date()


workout_dates = [get_date_from_filename(s) for s in lst_files]
df_workouts = pd.DataFrame(zip(workout_dates, lst_files),
                           columns=['date', 'file'])


def get_date_last_monday():
    """Return date object corresponding to last Monday."""
    today = dt.datetime.now()
    ind = today.weekday()
    t = today - dt.timedelta(days=ind)
    return t.date()


def get_date_n_days_ago(n):
    """Return date object for n days ago."""
    today = dt.datetime.now()
    out = today - dt.timedelta(days=n)
    return out.date()


tstart = get_date_last_monday()
tend = get_date_n_days_ago(0)

df_selection = df_workouts.query('date >= @tstart and date <= @tend')


zone_ranges = {'z1/z2': (113, 154), 'z3': (155, 164),
               'z4': (165, 173), 'z5': (174, 200)}


def create_df_with_hrs(lst):
    out = pd.DataFrame([])
    for f in lst:
        df = create_pandas_with_hrs(f)
        out = out.append(df)
    return out


def calc_time_each_zone(df):
    lst = []
    for key in zone_ranges:
        l, u = zone_ranges[key]
        df_new = df.query('HRs >= @l and HRs <= @u')
        lst.append(df_new.loc[:, 'Secs'].sum())
    return lst
