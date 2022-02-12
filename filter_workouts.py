
def filter_workouts_by_type(df, key='running'):
    """Filter workouts based on whether they are cycling, running, or
    cardio activities."""
    cond_running = "type == 'treadmill_running' or type == 'running'"
    cond_cycling = "type == 'indoor_cycling' or type == 'cyclying'"
    cond_cardio = cond_running + " or " + cond_cycling
    if key == 'running':
        out = df.query(cond_running)
    elif key == 'cycling':
        out = df.query(cond_cycling)
    elif key == 'cardio':
        out = df.query(cond_cardio)
    out.reset_index(drop=True, inplace=True)
    return out
