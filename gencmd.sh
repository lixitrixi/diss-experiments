#!/bin/bash
cd "$(dirname "$0")"

export SOLVERS="smt-lia-arrays smt-lia-atomic smt-bv-arrays smt-bv-atomic"

gen_for_file() {
    for SOLVER in $SOLVERS; do
        echo "--solver=$SOLVER $1"
    done
}
export -f gen_for_file

find problems -name '*.essence' | parallel gen_for_file > commands.txt
