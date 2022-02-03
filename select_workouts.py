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


workout_dates = [get_date_from_filename(s) for s in lst_files]
df_workouts = pd.DataFrame(zip(workout_dates, lst_files),
                           columns=['date', 'file'])

tstart = get_date_last_monday()
tend = get_date_n_days_ago(0)
df_selection = df_workouts.query('date >= @tstart and date <= @tend')
