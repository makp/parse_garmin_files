import matplotlib.pyplot as plt

from filter_workouts import filter_workouts_by_date_and_type
from calc_HR_zones import add_hr_zones


df = filter_workouts_by_date_and_type(7)


if df.empty:
    print("No workouts listed!!")


df = add_hr_zones(df)
df

# def calc_perc_per_zone(df):
#     total_per_zone = df.loc[:, 'z2':].sum()
#     total_time = total_per_zone.sum()
#     return total_per_zone/total_time


df.plot(x='date', y=['z2', 'z3', 'z4', 'z5'], width=0.9, kind='bar',
        color=['tab:blue', 'tab:green', 'gold', 'tab:red'])
plt.ion()
plt.show()
