#!/bin/bash

PA=$HOME'/CN/tp1'
TEST_VERSION=3

DATA=house

START="$1"

END="$2"

GEN="$3"


OUTBASE="${PA}/tests/${DATA}/${TEST_VERSION}/${GEN}/out_"

OUTFILE="${OUTBASE}${DATA}_${START}_${END}"

# mkdir $PA/tests/$DATA/$TEST_VERSION
# mkdir $PA/tests/$DATA/$TEST_VERSION/$POP
# for i in $(seq $START $END); do
#     echo $i;
#     $PA/source/main.py --crossover 0.9 --mutation 0.05 --seed $i --gen 50 --pop_size $POP --train $PA/datasets/$DATA-train.csv --test $PA/datasets/$DATA-test.csv --stats $OUTFILE --test_out $OUTFILE> "${OUTBASE}${DATA}_${i}"
# done


mkdir $PA/tests/$DATA/$TEST_VERSION
mkdir $PA/tests/$DATA/$TEST_VERSION/$GEN
for i in $(seq $START $END); do
    echo $i;
    $PA/source/main.py --crossover 0.9 --mutation 0.05 --seed $i --gen $GEN --pop_size 500 --train $PA/datasets/$DATA-train.csv --test $PA/datasets/$DATA-test.csv --stats $OUTFILE --test_out $OUTFILE> "${OUTBASE}${DATA}_${i}"
done