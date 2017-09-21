#!/bin/bash

PA=$HOME'/CN/tp1'
# TEST_VERSION=2

BASE=$PA/tests

# for f in keijzer-7 keijzer-10 house; do
#     mkdir $PA/graphs/$f

#     for D in $PA/tests/$f/*/; do
#         TEST_VERSION=$(basename $D)
#         echo $DIR

#         mkdir $PA/graphs/$f/$TEST_VERSION

#         for p in 50 100 500; do

#             mkdir $PA/graphs/$f/$TEST_VERSION/$p
#             DIR=$PA/tests/$f/$TEST_VERSION/$p
            
#             echo $DIR
#             ls $DIR | grep __ | while read -r line ; do
#                 echo "Processing $line"
#                 $PA/source/plot.py $DIR/$line $PA/graphs/$f/$TEST_VERSION/$p
#             done
#         done
#     done
# done


for f in keijzer-7 keijzer-10 house; do
    mkdir $PA/graphs/$f

    # for D in $PA/tests/$f/*/; do
        # TEST_VERSION=$(basename $D)
        TEST_VERSION=3
        echo $DIR

        mkdir $PA/graphs/$f/$TEST_VERSION

        for p in 50 100 500; do

            mkdir $PA/graphs/$f/$TEST_VERSION/$p
            DIR=$PA/tests/$f/$TEST_VERSION/$p
            
            echo $DIR
            ls $DIR | grep __ | while read -r line ; do
                echo "Processing $line"
                $PA/source/plot.py $DIR/$line $PA/graphs/$f/$TEST_VERSION/$p
            done
        done
    # done
done
