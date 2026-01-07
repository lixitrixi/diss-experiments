import pandas as pd

SOLVER_WALL_TIME_CUTOFF = 12 * 60 * 60  # 12 hours


def read_and_clean(csv):
    df = pd.read_csv(csv, skipinitialspace=True)

    # Normalize problem names
    df["problem"] = (
        df["problem"].str.replace("problems/", "").str.replace(".essence", "")
    )

    # Filter timeouts and clamp small values
    df = df[df["solver_wall_time_s"] <= SOLVER_WALL_TIME_CUTOFF]
    df["solver_wall_time_s"] = df["solver_wall_time_s"].clip(lower=10**-2)

    return df
