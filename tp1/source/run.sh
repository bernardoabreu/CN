#!/bin/bash

HOST=$(hostname)

echo $HOST
PA=$HOME'/CN/tp1'
TEST_VERSION=7
DATA=(keijzer-7 keijzer-10)
SUBDIRS=(50 100 500)
OUT=tests2

ELITISM=1
CROSS=0.9
MUT=0.05
TOUR=2
GEN=100
POP=500

while getopts 'd:v:o:s:h' opt ; do
  case $opt in
    d) DATA=("$OPTARG");;
    v) TEST_VERSION=$OPTARG;;
    o) OUT=$OPTARG;;
    s) SUBDIRS=("$OPTARG");;
    h) echo "Options: -d datasets (def: ${DATA[*]})";
       echo "         -v test version (def: ${TEST_VERSION})";
       echo "         -o output directory (def: ${OUT})";
       echo "         -s subdirectories (def: ${SUBDIRS[*]})";
       exit 0 ;;
  esac
done


# skip over the processed options
shift $((OPTIND-1))


echo $$ > "${PA}/norun_${HOST}.pid"


for f in ${DATA[*]}; do

    DIR=$PA/$OUT/$f/$TEST_VERSION/

    for SUBDIR in ${SUBDIRS[*]}; do
        mkdir -p $PA/$OUT/$f/$TEST_VERSION/$SUBDIR

        GEN=$SUBDIR

        for i in {1..30}; do
            $PA/source/main.py --elitism $ELITISM --crossover $CROSS --mutation $MUT --tournament $TOUR --seed $i --gen $GEN --pop_size $POP --train $PA/datasets/$f-train.csv --test $PA/datasets/$f-test.csv --stats "${DIR}${SUBDIR}/out_${f}" --test_out "${DIR}${SUBDIR}/out_${f}" > "${DIR}${SUBDIR}/${f}_${i}"
        done
    done

done
