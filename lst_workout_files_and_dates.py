"""Return a Pandas Dataframe containing the path to every Garmin .TCX
file and its date in the local time zone---instead of the UTC time
standard."""

import pandas as pd
import glob
import dateutil
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
    lst_files = glob.glob(path_to_garmin_files + '*.tcx')
    lst_dates = [get_date_from_filename(f) for f in lst_files]
    df = pd.DataFrame(zip(lst_dates, lst_files),
                      columns=['date', 'file'])
    df.sort_values(by=['date'], inplace=True)
    return df.reset_index(drop=True)


create_df()
