from get_hr_from_tcx import create_pandas_with_hrs
import pandas as pd


zone_ranges = {'z2': (130, 154), 'z3': (155, 164),
               'z4': (165, 173), 'z5': (174, 200)}


def create_lst_with_zones(filepath):
    """Return a list with the total number of seconds spent at each
    zone---as specified by 'zone-ranges.'"""
    df = create_pandas_with_hrs(filepath)
    lst = []
    for val in zone_ranges.values():
        l, u = val
        t = len(df[(df >= l) & (df <= u)])
        lst.append(t)
    return lst


def create_df_with_zones(lst_filepath):
    """Return a pandas dataframe from a list of .TCX files in which the
    columns list the amount of time spend at each HR zone---as
    specified by the variable 'zone_ranges.'"""
    df = pd.DataFrame([], columns=list(zone_ranges.keys()))
    for _ in lst_filepath:
        lst = create_lst_with_zones(_)
        df.loc[df.shape[0]] = lst
    return df


def add_hr_zones(df):
    """Add columns with the time spent at each zone."""
    df_zones = create_df_with_zones(df['file'])
    out = pd.concat([df, df_zones], axis=1)
    out.loc[:, 'z2':'z5'] = round(out.loc[:, 'z2':'z5']/60, 1)
    return out
