from lst_workout_between_dates import select_workouts_between_dates


def filter_workouts_by_type(df, key='running'):
    """Filter workouts based on whether they are cycling, running, or
    aerobic activities."""
    cond_running = "type == 'treadmill_running' or type == 'running'"
    cond_cycling = "type == 'indoor_cycling' or type == 'cyclying'"
    cond_aerobic = cond_running + " or " + cond_cycling
    if key == 'running':
        out = df.query(cond_running)
    elif key == 'cycling':
        out = df.query(cond_cycling)
    elif key == 'aerobic':
        out = df.query(cond_aerobic)
    out.reset_index(drop=True, inplace=True)
    return out


df = select_workouts_between_dates(14)
