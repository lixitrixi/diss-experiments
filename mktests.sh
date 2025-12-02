#!/bin/bash
cd "$(dirname "$0")"

export SOLVERS="smt-lia-arrays smt-lia-atomic smt-bv-arrays smt-bv-atomic"

mk_tests() {
    echo "conjure-oxide solve --solver=$SOLVER $1"
    echo "conjure-oxide solve --solver=$SOLVER --use-optimised-rewriter $1"
}
export -f mk_tests

mk_for_problem_file() {
    for SOLVER in $SOLVERS; do
        mk_tests $1
    done
}
export -f mk_for_problem_file

find problems -name '*.essence' | parallel mk_for_problem_file > tests.txt
