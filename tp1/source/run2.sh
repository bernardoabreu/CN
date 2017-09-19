#!/bin/bash

PA=$HOME'/CN/tp1'
TEST_VERSION=2

DATA=house

START="$1"

END="$2"

POP="$3"

OUTFILE="${DATA}_${START}_${END}"

mkdir $PA/tests/$DATA/$TEST_VERSION
mkdir $PA/tests/$DATA/$TEST_VERSION/$POP
for i in $(seq $START $END); do
    echo $i;
    $PA/source/main.py --crossover 0.9 --mutation 0.05 --seed $i --pop_size $POP --train $PA/datasets/$DATA-train.csv --test $PA/datasets/$DATA-test.csv --stats $PA/tests/$DATA/$TEST_VERSION/$POP/out_$OUTFILE >  $PA/tests/$DATA/$TEST_VERSION/$POP/out_"${DATA}_${i}"
done