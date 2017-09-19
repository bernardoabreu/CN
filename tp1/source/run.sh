#!/bin/bash

PA=$HOME'/CN/tp1'
TEST_VERSION=2


for f in keijzer-7 keijzer-10; do

    mkdir $PA/tests/$f/$TEST_VERSION

    for p in 50 100 500; do

        mkdir $PA/tests/$f/$TEST_VERSION/$p

        for i in {1..30}; do
            $PA/source/main.py --crossover 0.9 --mutation 0.05 --seed $i --pop_size $p --train $PA/datasets/$f-train.csv --test $PA/datasets/$f-test.csv --stats $PA/tests/$f/$TEST_VERSION/$p/out_$f > $PA/tests/$f/$TEST_VERSION/$p/out_"${f}_${i}"
        done
    done
done