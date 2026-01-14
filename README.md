# Dissertation Experiments

Performance and correctness testing for my 5th year dissertation. See [Conjure Oxide](https://github.com/conjure-cp/conjure-oxide)

## Installation

Install [Conjure Oxide](https://github.com/conjure-cp/conjure-oxide) as an executable. Instructions to install from source can be found in the project's README.

This project uses [GNU parallel](https://www.gnu.org/software/parallel/) to test several problem instances efficiently in high-performance computing environments.

Install [jq](https://jqlang.org/) for command-line JSON parsing.

### Python Environment

Create a python environment in the project directory (3.11+) and run:

```
    .venv/bin/activate && pip install -r requirements.txt
```

## How to Use

An experiment can be run with `runtests.sh`. Although this is parallelised it can still take on the order of days to gather data.

The resulting output CSV can be run through various visualisations. With the virtual environment active, run:

    python visualisation/all.py <output.csv> figs

This will place the visualisation in a folder `figs`.
