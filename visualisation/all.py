import os, sys, utils
import pandas as pd
from line_chart import all_line_charts
from speedup_grid import all_speedup_grids


def all_figs(df: pd.DataFrame, outdir: str):
    all_line_charts(df, outdir)
    all_speedup_grids(df, outdir)


if __name__ == "__main__":
    csv, outdir = sys.argv[1:3]
    os.makedirs(outdir, exist_ok=True)
    df = utils.read_and_clean(csv)
    all_figs(df, outdir)
