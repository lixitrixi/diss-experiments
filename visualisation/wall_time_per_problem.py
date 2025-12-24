import sys, os, pandas as pd, matplotlib.pyplot as plt

SOLVER_WALL_TIME_CUTOFF = 12 * 60 * 60  # 12 hours


def wall_time_per_problem(df: pd.DataFrame, outdir: str):
    """A line chart with X=problem instance and Y=solver wall time.
    Each line represents a specific solver configuration."""

    # Normalize problem names
    df["problem"] = (
        df["problem"].str.replace("problems/", "").str.replace(".essence", "")
    )

    # Filter timeouts and clamp small values
    df = df[df["solver_wall_time_s"] <= SOLVER_WALL_TIME_CUTOFF]
    df["solver_wall_time_s"] = df["solver_wall_time_s"].clip(lower=10**-2)

    # Compute virtual best solver (VBS)
    best = df.loc[df.groupby("problem")["solver_wall_time_s"].idxmin()].copy()
    best["solver"] = "VBS"

    # Sort problems by VBS wall time
    problem_order = best.sort_values("solver_wall_time_s")["problem"].tolist()

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

    df = pd.concat([df, best])

    plt.figure(figsize=(10, 6))
    for solver in df["solver"].unique():
        s = df[df["solver"] == solver].sort_values("problem")
        linestyle = "--" if solver == "VBS" else "-"
        plt.plot(
            s["problem"], s["solver_wall_time_s"], label=solver, linestyle=linestyle
        )

    plt.yscale("log")
    plt.legend()
    plt.title("Solver Wall Time per Problem Instance")
    plt.xlabel("Problem Instance")
    plt.ylabel("Solver Wall Time (s)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    plt.savefig(f"{outdir}/wall_time_per_problem.png")
    plt.close()


if __name__ == "__main__":
    csv, outdir = sys.argv[1:3]
    os.makedirs(outdir, exist_ok=True)
    df = pd.read_csv(csv, skipinitialspace=True)
    wall_time_per_problem(df, outdir)
