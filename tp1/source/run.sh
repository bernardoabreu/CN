#!/bin/bash

PA=$HOME'/CN/tp1'
TEST_VERSION=1


mkdir $PA/tests/keijzer-7/$TEST_VERSION
mkdir $PA/tests/keijzer-10/$TEST_VERSION
mkdir $PA/tests/house/$TEST_VERSION

for p in 50 100 500;
do
    mkdir $PA/tests/keijzer-7/$TEST_VERSION/$p
    mkdir $PA/tests/keijzer-10/$TEST_VERSION/$p
    mkdir $PA/tests/house/$TEST_VERSION/$p

    for i in {1..30}; do
        $PA/source/main.py --seed $i --pop_size $p --train $PA/datasets/keijzer-7-train.csv --test $PA/datasets/keijzer-7-test.csv --stats $PA/tests/keijzer-7/$TEST_VERSION/$p/out_7 > $PA/tests/keijzer-7/$TEST_VERSION/$p/out_7_$i
    done

    for i in {1..30}; do
        $PA/source/main.py --seed $i --pop_size $p --train $PA/datasets/keijzer-10-train.csv --test $PA/datasets/keijzer-10-test.csv --stats $PA/tests/keijzer-10/$TEST_VERSION/$p/out_10 > $PA/tests/keijzer-10/$TEST_VERSION/$p/out_10_$i
    done

    for i in {1..30}; do
        $PA/source/main.py --seed $i --pop_size $p --train $PA/datasets/house-train.csv --test $PA/datasets/house-test.csv --stats $PA/tests/house/$TEST_VERSION/$p/out_house >  $PA/tests/house/$TEST_VERSION/$p/out_house_$i
    done
done