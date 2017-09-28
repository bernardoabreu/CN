#!/bin/bash

HOST=$(hostname)

echo $HOST
PA=$HOME'/CN/tp1'
TEST_VERSION=7
DATA_SETS=(house)
SUBDIRS=(50 100 500)
OUT=tests2

ELITISM=1
CROSS=0.9
MUT=0.05
TOUR=2
GEN=50
POP=500

while getopts 'd:v:o:s:h' opt ; do
  case $opt in
    d) DATA_SETS=("$OPTARG");;
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


if [ $# -lt 2 ]; then
  echo "Usage: $0 [options] RangeStart RangeEnd"
  echo "Options: -d datasets (def: ${DATA[*]})";
  echo "         -v test version (def: ${TEST_VERSION})";
  echo "         -o output directory (def: ${OUT})";
  echo "         -s subdirectories (def: ${SUBDIRS[*]})";
  exit 1
fi

START="$1"
END="$2"


echo $$ > "${PA}/norun2_${HOST}_${DATA_SETS[*]}_${START}_${END}.pid"


for $DATA in ${DATA_SETS[*]}; do

  for SUBDIR in ${SUBDIRS[*]}; do
    OUTBASE="${PA}/${OUT}/${DATA}/${TEST_VERSION}/${SUBDIR}/out_"
    OUTFILE="${OUTBASE}${DATA}_${START}_${END}"

    for i in $(seq $START $END); do
        echo $i;
        $PA/source/main.py --elitism $ELITISM --crossover $CROSS --mutation $MUT --tournament $TOUR --seed $i --gen $GEN --pop_size $POP --train $PA/datasets/$DATA-train.csv --test $PA/datasets/$DATA-test.csv --stats $OUTFILE --test_out $OUTFILE> "${OUTBASE}${DATA}_${i}"
    done
  done
done