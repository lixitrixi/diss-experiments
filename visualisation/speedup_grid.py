import sys, os, pandas as pd, matplotlib.pyplot as plt, numpy as np
from matplotlib.lines import Line2D
import utils


def speedup_grid(df: pd.DataFrame, outdir: str):
    """A grid of scatterplots allowing each solver to be compared against the others.
    Each (x, y) is the wall time of one solver plotted against the wall time of the other.
    """

    # Only compare against lower Savile Row optimisation
    df = df[df["solver"].apply(lambda name: "-O2" not in name)]

    # Extract problem group (first directory)
    df["problem_group"] = df["problem"].apply(lambda p: p.split("/")[0])

    solvers = df["solver"].unique()
    solvers.sort()
    num_solvers = len(solvers)

    min_t = 10**-2
    max_t = utils.SOLVER_WALL_TIME_CUTOFF * 1.5

    # Assign a marker per problem group
    marker_cycle = ["o", "s", "^", "v", "D", "P", "X", "*", "<", ">", "h"]
    groups = sorted(df["problem_group"].unique())
    marker_by_group = {
        g: marker_cycle[i % len(marker_cycle)] for i, g in enumerate(groups)
    }
    color_cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    color_by_group = {
        g: color_cycle[i % len(color_cycle)] for i, g in enumerate(groups)
    }
    legend_handles = [
        Line2D(
            [0],
            [0],
            marker=marker_by_group[group],
            linestyle="none",
            markerfacecolor="none",
            markeredgecolor=color_by_group[group],
            markeredgewidth=0.8,
            markersize=6,
            label=group,
        )
        for group in groups
    ]

    fig, axs = plt.subplots(num_solvers, num_solvers, figsize=(10, 10))

    for i, s1 in enumerate(solvers):
        for j, s2 in enumerate(solvers):
            ax: plt.Axes = axs[i, j]
            ax.set_box_aspect(1)

            ax.set_xscale("log")
            ax.set_yscale("log")
            ax.set_xlim(min_t, max_t)
            ax.set_ylim(min_t, max_t)

            if i == j:
                # ax.axis("off")
                continue

            x = np.linspace(min_t, max_t)
            ax.plot(x, x, color="blue", lw=0.3)

            s1_by_prob = df[df["solver"] == s1].set_index("problem")
            s2_by_prob = df[df["solver"] == s2].set_index("problem")
            joined = s1_by_prob.join(s2_by_prob, lsuffix="_s1", rsuffix="_s2")

            # Plot each problem group with its own marker
            for group, marker in marker_by_group.items():
                g = joined[joined["problem_group_s1"] == group]
                if g.empty:
                    continue

                ax.scatter(
                    g["solver_wall_time_s_s1"],
                    g["solver_wall_time_s_s2"],
                    marker=marker,
                    s=20,
                    facecolors="none",
                    edgecolors=color_by_group[group],
                    linewidths=0.8,
                )

    legend_ax = axs[-1, -1]

    legend_ax.legend(
        handles=legend_handles,
        title="Problem type",
        loc="center",
        fontsize="small",
        title_fontsize="small",
        frameon=True,
    )

    for ax, col in zip(axs[-1], solvers):
        ax.set_xlabel(col, rotation=0)

    for ax, row in zip(axs[:, 0], solvers):
        ax.set_ylabel(row, rotation=90)

    fig.tight_layout()

    plt.savefig(f"{outdir}/speedup_grid.png")
    plt.close()


if __name__ == "__main__":
    csv, outdir = sys.argv[1:3]
    os.makedirs(outdir, exist_ok=True)
    df = utils.read_and_clean(csv)
    speedup_grid(df, outdir)
