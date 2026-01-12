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
    iteration=$3
    smtfile=$(mktemp -p tmp)
    statfile=$(mktemp -p tmp)

    # This substring indicates it's safe to use the optimised rewriter
    if grep -q experiment-use-optimised-rewriter $probfile; then
        rewriter_arg="--use-optimised-rewriter"
    else
        rewriter_arg=""
    fi

    # Write to SMTLIB file, then run z3 directly on it
    conjure-oxide solve \
        -s="$solver" \
        --save-solver-input-file="$smtfile" \
        --no-run-solver \
        --info-json-path="$statfile" \
        $rewriter_arg \
        $probfile > /dev/null 2>> $ERR_FILE

    echo '(get-info :all-statistics)' >> $smtfile

    result=$(z3 $smtfile)

    info "DONE ($solver): $probfile"

    secs=$(jq -r '.stats.rewriterRuns.[0].rewriterRunTime.secs' < $statfile)
    nanos=$(jq -r '.stats.rewriterRuns.[0].rewriterRunTime.nanos' < $statfile)
    rewritetime=$(echo "$secs + $nanos/10^9" | bc -l)

    solvetime=$(echo $result | grep ':time' | sed -E 's/.*:time[[:space:]]+([0-9.]+).*/\1/')

    echo "conjure-oxide, $solver, $probfile, $iteration, $solvetime, $rewritetime"
}

# Run Conjure and print the solver time
bench_conjure() {
    solver=$1
    opt_level=$2
    probfile=$3
    iteration=$4
    outdir=$(mktemp -d -p tmp)

    conjure solve \
        --solver="$solver" \
        -o="$outdir" \
        --copy-solutions=off \
        --savilerow-options="-O$opt_level" \
        $probfile > /dev/null 2>> $ERR_FILE

    info "DONE ($solver (-O$opt_level)): $probfile"

    solvetime=$(jq -r '.savilerowInfo.SolverTotalTime' < $outdir/*.stats.json)

    totaltime=$(jq -r '.totalTime' < $outdir/*.stats.json)
    rewritetime=$(echo "$totaltime - $solvetime" | bc -l)

    echo "conjure, $solver (-O$opt_level), $probfile, $iteration, $solvetime, $rewritetime"
}

# /// Run Tests ///

export ERR_FILE
export -f bench_conjure bench_oxide info err

mkdir -p tmp
mkdir -p output
echo $COLUMNS > $RESULTS_FILE

parallel -j80 --no-notice --progress --eta --memfree 100G --resume-failed --joblog "output/jobs_$NOW.tsv" '{}' \
    :::: cmd-prefixes.sh \
    ::: $(find problems -name '*.essence' | sort) \
    ::: $(seq $REPEATS) >> $RESULTS_FILE

echo "results written to $RESULTS_FILE"
cat $RESULTS_FILE
