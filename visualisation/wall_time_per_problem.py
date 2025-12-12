import sys, os, pandas as pd, matplotlib.pyplot as plt


def wall_time_per_problem(df: pd.DataFrame, outdir: str):
    """A line chart with X=problem instance and Y=solver wall time.
    Each line represents a specific solver configuration."""

    # Strip leading "problems/" and trailing ".essence" from problem names
    df["problem"] = (
        df["problem"].str.replace("problems/", "").str.replace(".essence", "")
    )

    df = df.sort_values(by=["problem"])

    # Calculate the virtual best solver and treat as its own solver
    best = df.loc[df.groupby("problem")["solver_wall_time_s"].idxmin()]
    best["solver"] = "VBS"
    df = pd.concat([df, best])

    plt.figure(figsize=(10, 6))
    for solver in df["solver"].unique():
        s = df[df["solver"] == solver]
        plt.plot(s["problem"], s["solver_wall_time_s"], label=solver)

    plt.yscale("log")

    plt.legend()
    plt.title("Solver Wall Time per Problem Instance")
    plt.xlabel("Problem Instance")
    plt.ylabel("Solver Wall Time (s)")

    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    # Create the output directory if it does not exist
    plt.savefig(f"{outdir}/wall_time_per_problem.png")
    plt.close()


if __name__ == "__main__":
    csv, outdir = sys.argv[1:3]
    os.makedirs(outdir, exist_ok=True)
    df = pd.read_csv(csv, skipinitialspace=True)
    wall_time_per_problem(df, outdir)
