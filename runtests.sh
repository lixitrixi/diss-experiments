#!/bin/bash
cd "$(dirname "$0")"
set -euxo pipefail

REPEATS=1
NOW="$(date +%Y-%m-%d_%H-%M-%S)"
ERR_FILE="output/err_$NOW.log"
RESULTS_FILE="output/results_$NOW.csv"
COLUMNS="tool, solver, problem, repeat_iteration, solver_wall_time_s, rewriter_wall_time_s"

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

    info "DONE (oxide): $probfile"

    secs=$(jq -r '.stats.rewriterRuns.[0].rewriterRunTime.secs' < $statfile)
    nanos=$(jq -r '.stats.rewriterRuns.[0].rewriterRunTime.nanos' < $statfile)
    rewritetime=$(echo "$secs + $nanos/10^9" | bc -l)

    solvetime=$(jq -r '.stats.solverRuns.[0].conjureSolverWallTime_s' < $statfile)

    echo "conjure-oxide, $solver, $probfile, $3, $solvetime, $rewritetime"
}

# Run Conjure and print the solver time
bench_conjure() {
    solver=$1
    probfile=$2
    outdir=$(mktemp -d)

    conjure solve \
        --solver $solver \
        -o $outdir \
        --copy-solutions=off \
        $probfile > /dev/null 2>> $ERR_FILE
    
    info "DONE (conjure): $probfile"

    solvetime=$(jq -r '.savilerowInfo.SolverTotalTime' < $outdir/*.stats.json)

    totaltime=$(jq -r '.totalTime' < $outdir/*.stats.json)
    rewritetime=$(echo "$totaltime - $solvetime" | bc -l)

    echo "conjure, z3, $probfile, $3, $solvetime, $rewritetime"
}

# /// Run Tests ///

export ERR_FILE
export -f bench_conjure bench_oxide info err

mkdir -p output
echo $COLUMNS > $RESULTS_FILE

parallel --progress '{}' \
    :::: cmd-prefixes \
    ::: $(find problems -name '*.essence' | sort) \
    ::: $(seq $REPEATS) >> $RESULTS_FILE

echo "results written to $RESULTS_FILE"
cat $RESULTS_FILE
