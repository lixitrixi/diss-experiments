#!/bin/bash
cd "$(dirname "$0")"

> out.txt
> err.txt

FORMAT="User: %U seconds, System: %S seconds, Real: %e seconds"

run_test() {
    time bash -c "$1" >> out.txt 2>> err.txt
}
export -f run_test

parallel run_test :::: tests.txt > "times_$(date +%Y-%m-%d_%H-%M-%S).txt" 2>&1
