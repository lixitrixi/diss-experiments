#!/bin/bash
cd "$(dirname "$0")"
set -euxo pipefail

REPEATS=1
NOW="$(date +%Y-%m-%d_%H-%M-%S)"
ERR_FILE="output/err_$NOW.log"
RESULTS_FILE="output/results_$NOW.csv"

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

    conjure-oxide solve \
        -n 1 \
        -s $solver \
        --info-json-path $statfile \
        $probfile > /dev/null 2>> $ERR_FILE

    info "DONE: $probfile"

    secs=$(jq '.stats.rewriterRuns.[0].rewriterRunTime.secs' < $statfile)
    nanos=$(jq '.stats.rewriterRuns.[0].rewriterRunTime.nanos' < $statfile)
    rewritetime=$(echo "$secs + $nanos/10^9" | bc -l)

    solvetime=$(jq '.stats.solverRuns.[0].conjureSolverWallTime_s' < $statfile)

    echo "conjure-oxide, $solver, $probfile, $3, $solvetime, $rewritetime"
}

# Run Conjure and print the solver time
bench_conjure() {
    probfile=$1
}

# /// Run Tests ///

export ERR_FILE
export -f bench_conjure bench_oxide info err

mkdir -p output
echo "tool, solver, problem, repeat_iteration, solver_wall_time_s, rewriter_wall_time_s" > $RESULTS_FILE

parallel --progress '{}' \
    :::: cmd-prefixes \
    ::: $(find problems -name '*.essence' | sort) \
    ::: $(seq $REPEATS) >> $RESULTS_FILE

echo "results written to $RESULTS_FILE"
cat $RESULTS_FILE
