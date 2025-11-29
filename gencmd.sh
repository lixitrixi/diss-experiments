#!/bin/bash

cd $(dirname $0)

OXIDE_SOLVERS="smt-lia-arrays smt-lia-atomic smt-bv-arrays smt-bv-atomic"

gen_for_file () {
    echo $1
}

for f in problems/**/* ; do
    gen_for_file $f
done
