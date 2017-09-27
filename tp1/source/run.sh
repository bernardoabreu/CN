#!/bin/bash

HOST=$(hostname)

echo $HOST
PA=$HOME'/CN/tp1'
TEST_VERSION=7
DATA=(keijzer-7 keijzer-10)
SUBDIRS=(keijzer-7 keijzer-10)
OUT=tests2

while getopts 'd:v:o:s:h' opt ; do
  case $opt in
    d) DATA=("$OPTARG");;
    v) TEST_VERSION=$OPTARG;;
    o) OUT=$OPTARG;;
    s) SUBDIRS=("$OPTARG");;
    h) echo "Options: -d datasets (def: ${DATA[*]})";
       exit 0 ;;
  esac
done


# skip over the processed options
shift $((OPTIND-1))


echo $$ > "${PA}/norun_${HOST}.pid"


for f in ${DATA[*]}; do

    DIR=$PA/$OUT/$f/$TEST_VERSION
    mkdir $DIR

    for SUBDIR in ${SUBDIRS[*]}; do
        mkdir -p $PA/$OUT/$f/$TEST_VERSION/$SUBDIR

        for i in {1..30}; do
            $PA/source/main.py --elitism 0 --crossover 0.9 --mutation 0.05 --tournament 7 --seed $i --gen 100 --pop_size 500 --train $PA/datasets/$f-train.csv --test $PA/datasets/$f-test.csv --stats "${DIR}${SUBDIR}/out_${f}" --test_out "${DIR}${SUBDIR}/out_${f}" > "${DIR}${SUBDIR}/${f}_${i}"
        done
    done

done
