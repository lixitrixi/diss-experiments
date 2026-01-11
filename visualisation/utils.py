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
    # df["solver_wall_time_s"] = df["solver_wall_time_s"].clip(
    #     lower=10**-2, upper=SOLVER_WALL_TIME_CUTOFF
    # )

    # Extract problem group (first directory)
    df["problem_group"] = df["problem"].apply(lambda p: p.split("/")[0])

    return df


# Calculates the VBS and returns (sorted, VBS, sorted+VBS)
def add_vbs_and_sort(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    solvers = df["solver"].unique()
    # print(f"Solvers: {solvers}")

    # Compute virtual best solver (VBS)
    best = df.loc[
        df.groupby("problem", observed=True)["solver_wall_time_s"].idxmin()
    ].copy()
    best["solver"] = "VBS"

    # Sort problems by VBS wall time
    problem_order = best.sort_values("solver_wall_time_s")["problem"].tolist()
    # print(f"Problem order: {problem_order}")

    # Apply this ordering to all data
    df["problem"] = pd.Categorical(
        df["problem"],
        categories=problem_order,
        ordered=True,
    )
    best["problem"] = pd.Categorical(
        best["problem"],
        categories=problem_order,
        ordered=True,
    )

    return df, best, pd.concat([df, best])
