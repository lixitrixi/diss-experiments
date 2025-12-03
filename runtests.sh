#!/bin/bash
cd "$(dirname "$0")"
set -euxo pipefail

export NOW="$(date +%Y-%m-%d_%H-%M-%S)"
REPEATS=1

info() {
  echo "-- info: $*" >/dev/stderr
}

err() {
    echo "-- fatal: $*" >/dev/stderr
}

# Run Conjure Oxide and print the solver time
bench_oxide() {
    solver=$1
    probfile=$2
    statfile=$(mktemp)

    conjure-oxide solve -n 1 \
        -s $solver \
        --info-json-path=$statfile \
        --use-optimised-rewriter \
        $probfile > /dev/null 2>> "output/err_$NOW.csv"

    info "DONE: $probfile"

    solvetime=$(jq '.stats.solverRuns.[0].conjureSolverWallTime_s' < $statfile)
    echo "conjure-oxide, $solver, $probfile, $3, $solvetime"
}

# Run Conjure and print the solver time
bench_conjure() {
    probfile=$1
}

export -f bench_conjure bench_oxide info err

mkdir -p output
echo "tool, solver, problem, repeat_iteration, solver_wall_time" > \
    "output/results_$NOW.csv"

parallel --progress '{}' \
    :::: cmd-prefixes \
    ::: $(find problems -name '*.essence' | sort) \
    ::: $(seq $REPEATS) >> "output/results_$NOW.csv"
