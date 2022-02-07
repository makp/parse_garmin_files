from get_hr_from_tcx import create_pandas_with_hrs
import pandas as pd


zone_ranges = {'z1/z2': (113, 154), 'z3': (155, 164),
               'z4': (165, 173), 'z5': (174, 200)}


def create_dic_with_hrs(filepath):
    """Create a dictionary with time in seconds for each of the zones
    as specified by 'zone-ranges.'"""
    df = create_pandas_with_hrs(filepath)
    dic = {}
    for key in zone_ranges:
        l, u = zone_ranges[key]
        df_new = df.query('HRs >= @l and HRs <= @u')
        dic[key] = df_new.loc[:, 'Secs'].sum()
    return dic


def create_pandas_with_zones(lst_filepath):
    """Create pandas dataframe from a list of tcx files in which the
    columns list the amount of time spend at each HR zone---as
    specified by 'zone_ranges.'"""
    df = pd.DataFrame()
    for _ in lst_filepath:
        dic = create_dic_with_hrs(_)
        df = df.append(dic, ignore_index=True)
    return df
