from get_hr_from_tcx import create_pandas_with_hrs
import pandas as pd


filenames = ['teste']

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
