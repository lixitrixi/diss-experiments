# Dissertation Experiments

Performance and correctness testing for my 5th year dissertation. See [Conjure Oxide](https://github.com/conjure-cp/conjure-oxide)

## Installation

To just visualise the data, skip ahead to setting up the Python environment. To install the necessary tools for running the experiments:

- Install [Conjure Oxide](https://github.com/conjure-cp/conjure-oxide) as an executable. Instructions to install from source can be found in the project's README (`cargo install --path crates/conjure-cp-cli`).

- Install [Conjure](https://conjure.readthedocs.io/en/latest/installation.html) using instructions to install containers.

- Install the Z3 solver (included in the Conjure container install) as a command. For Docker, use:

        echo 'docker run --rm -v "$PWD:/work" -w /work ghcr.io/conjure-cp/conjure:v2.6.0 z3 "$@"' > ~/.local/bin/z3

    For Podman, use:

        echo 'podman run --rm -v "$PWD:/work:z" -w /work ghcr.io/conjure-cp/conjure:v2.6.0 z3 "$@"' > ~/.local/bin/z3

- Install [GNU parallel](https://www.gnu.org/software/parallel/).

- Ensure [jq](https://jqlang.org/) is installed (1.8.1+).

You should now be able to run the experiments or run the tools directly against problem instances in `problems/`. To run Conjure Oxide with the new SMT backend, use:

    conjure-oxide solve -n 1 -s smt-[bv|lia]-[arrays-atomic] <path/to/essence/file>

## Python Environment

Create a Python environment in the project directory (3.11+) and run:

    . .venv/bin/activate && pip install -r requirements.txt

## How to Use

An experiment can be started with:

    runtests.sh

Results will be placed in a uniquely named CSV file `output/results-*.csv` and error logs into `output/err-*.log`. If there are issues with column names, please use the ones defined in `runtests.sh`.

The results can be run through various visualisations. With the virtual environment active, run:

    python visualisation/all.py <output.csv> figs

This will place the visualisations in a folder `figs/`.
