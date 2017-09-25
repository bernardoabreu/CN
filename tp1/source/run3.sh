#!/bin/bash

HOST=$(hostname)

echo $HOST
PA=$HOME'/CN/tp1'
TEST_VERSION=6

echo $$ > "${PA}/norun_${HOST}.pid"

# for f in keijzer-7 keijzer-10; do

#     mkdir $PA/tests/$f/$TEST_VERSION

#     for p in 50 100 500; do

#         mkdir $PA/tests/$f/$TEST_VERSION/$p

#         for i in {1..30}; do
#             $PA/source/main.py --crossover 0.9 --mutation 0.05 --seed $i --pop_size $p --train $PA/datasets/$f-train.csv --test $PA/datasets/$f-test.csv --stats $PA/tests/$f/$TEST_VERSION/$p/out_$f > $PA/tests/$f/$TEST_VERSION/$p/out_"${f}_${i}"
#         done
#     done
# done

# for f in keijzer-7 keijzer-10; do

#     mkdir $PA/tests/$f/$TEST_VERSION

#     OUT="${PA}/tests/${f}/${TEST_VERSION}/"
#     for g in 100 500; do

#         mkdir $PA/tests/$f/$TEST_VERSION/$g

#         for i in {1..30}; do
#             $PA/source/main.py --crossover 0.9 --mutation 0.05 --seed $i --gen $g --pop_size 500 --train $PA/datasets/$f-train.csv --test $PA/datasets/$f-test.csv --stats "${OUT}${g}/out_${f}" --test_out "${OUT}${g}/out_${f}" > "${OUT}${g}/${f}_${i}"
#         done
#     done
# done



for f in keijzer-10; do

    mkdir $PA/tests/$f/$TEST_VERSION

    OUT="${PA}/tests/${f}/${TEST_VERSION}/"

    # mkdir $PA/tests/$f/$TEST_VERSION/cross_high

    # for i in {1..30}; do
    #     $PA/source/main.py --crossover 0.9 --mutation 0.05 --seed $i --gen 100 --pop_size 500 --train $PA/datasets/$f-train.csv --test $PA/datasets/$f-test.csv --stats "${OUT}cross_high/out_${f}" --test_out "${OUT}cross_high/out_${f}" > "${OUT}cross_high/${f}_${i}"
    # done


    mkdir -p $PA/tests/$f/$TEST_VERSION/0

    for i in {1..30}; do
        $PA/source/main.py --elitism 0 --crossover 0.9 --mutation 0.05 --tournament 7 --seed $i --gen 100 --pop_size 500 --train $PA/datasets/$f-train.csv --test $PA/datasets/$f-test.csv --stats "${OUT}0/out_${f}" --test_out "${OUT}0/out_${f}" > "${OUT}0/${f}_${i}"
    done

done
