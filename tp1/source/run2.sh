#!/bin/bash

PA='/home/bernardoabreu/CN/tp1'
TEST_VERSION=1

for p in 500;
do
    for i in {20..30}; do
        $PA/source/main.py --seed $i --pop_size $p --train $PA/datasets/house-train.csv --test $PA/datasets/house-test.csv --stats $PA/tests/house/$TEST_VERSION/$p/out_house >  $PA/tests/house/$TEST_VERSION/$p/out_house_$i
    done
done