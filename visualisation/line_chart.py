import sys, os, pandas as pd, matplotlib.pyplot as plt
import utils


def line_chart(df: pd.DataFrame, outdir: str, suffix: str):
    """A line chart with X=problem instance and Y=solver wall time.
    Each line represents a specific solver configuration."""
    df = df.copy()

    plt.figure(figsize=(10, 6))
    for solver in df["solver"].unique():
        s = df[df["solver"] == solver].sort_values("problem")
        linestyle = "--" if "VBS" in solver else "-"
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
    plt.axhline(y=utils.SOLVER_WALL_TIME_CUTOFF, color="r", linestyle="--", linewidth=1)

    plt.savefig(f"{outdir}/line_chart_{suffix}.png")
    plt.close()


def all_line_charts(df: pd.DataFrame, outdir: str):

    # Compare all solver configurations
    d, _, _ = utils.add_vbs_and_sort(df)
    line_chart(d, outdir, "all")

    # Only compare Conjure configurations
    d = df[df["solver"].apply(lambda name: "z3-" in name)]
    d, conjure_best, _ = utils.add_vbs_and_sort(d)
    line_chart(d, outdir, "conjure")

    # Only compare Conjure Oxide configurations
    d = df[df["solver"].apply(lambda name: "smt-" in name)]
    d, oxide_best, _ = utils.add_vbs_and_sort(d)
    line_chart(d, outdir, "oxide")

    oxide_best["solver"] = "oxide-VBS"
    d = df[df["solver"].apply(lambda name: "z3-" in name)]
    d = pd.concat([d, oxide_best])
    d, _, _ = utils.add_vbs_and_sort(d)
    line_chart(d, outdir, "all-oxide-vbs")

    for group in df["problem_group"].unique():
        dg = df[df["problem_group"] == group]

        d, _, _ = utils.add_vbs_and_sort(dg)
        line_chart(d, outdir, f"all-{group}")

        d = dg[dg["solver"].apply(lambda name: "z3-" in name)]
        d, conjure_best, _ = utils.add_vbs_and_sort(d)
        line_chart(d, outdir, f"conjure-{group}")

        d = dg[dg["solver"].apply(lambda name: "smt-" in name)]
        d, oxide_best, _ = utils.add_vbs_and_sort(d)
        line_chart(d, outdir, f"oxide-{group}")

        oxide_best["solver"] = "oxide-VBS"
        d = dg[dg["solver"].apply(lambda name: "z3-" in name)]
        d = pd.concat([d, oxide_best])
        d, _, _ = utils.add_vbs_and_sort(d)
        line_chart(d, outdir, f"all-oxide-vbs-{group}")


if __name__ == "__main__":
    csv, outdir = sys.argv[1:3]
    os.makedirs(outdir, exist_ok=True)
    df = utils.read_and_clean(csv)
    all_line_charts(df, outdir)
