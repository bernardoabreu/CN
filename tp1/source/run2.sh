#!/bin/bash

HOST=$(hostname)

PA=$HOME'/CN/tp1'

DATA=(house)

TEST_VERSION=4

TOUR="$3"

# parse the options
while getopts 'd:h' opt ; do
  case $opt in
  	d) DATA=("$OPTARG");;
	h) echo "Usage: $0 [options] RangeStart RangeEnd"; 
	   echo "Options: -d datasets (def: ${DATA[*]})";
	   exit 0 ;;
  esac
done

# skip over the processed options
shift $((OPTIND-1)) 

if [ $# -lt 2 ]; then
  echo "Usage: $0 [options] RangeStart RangeEnd"
  echo "Options: -d datasets (def: ${DATA[*]})"
  exit 1
fi

START="$1"
END="$2"



echo $$ > "${PA}/norun2_${HOST}_${DATA}_${START}_${END}.pid"

# OUTBASE="${PA}/tests/${DATA}/${TEST_VERSION}/${GEN}/out_"

# OUTFILE="${OUTBASE}${DATA}_${START}_${END}"

# mkdir $PA/tests/$DATA/$TEST_VERSION
# mkdir $PA/tests/$DATA/$TEST_VERSION/$POP
# for i in $(seq $START $END); do
#     echo $i;
#     $PA/source/main.py --crossover 0.9 --mutation 0.05 --seed $i --gen 50 --pop_size $POP --train $PA/datasets/$DATA-train.csv --test $PA/datasets/$DATA-test.csv --stats $OUTFILE --test_out $OUTFILE> "${OUTBASE}${DATA}_${i}"
# done


# mkdir $PA/tests/$DATA/$TEST_VERSION
# mkdir $PA/tests/$DATA/$TEST_VERSION/$GEN
# for i in $(seq $START $END); do
#     echo $i;
#     $PA/source/main.py --crossover 0.9 --mutation 0.05 --seed $i --gen $GEN --pop_size 500 --train $PA/datasets/$DATA-train.csv --test $PA/datasets/$DATA-test.csv --stats $OUTFILE --test_out $OUTFILE> "${OUTBASE}${DATA}_${i}"
# done

OUTBASE="${PA}/tests/${DATA}/${TEST_VERSION}/${TOUR}/out_"
OUTFILE="${OUTBASE}${DATA}_${START}_${END}"
# mkdir $PA/tests/$DATA/$TEST_VERSION

mkdir -p $PA/tests/$DATA/$TEST_VERSION/$TOUR
for i in $(seq $START $END); do
    echo $i;
    $PA/source/main.py --crossover 0.9 --mutation 0.05 --seed $i --gen 100 --pop_size 500 --train $PA/datasets/$DATA-train.csv --test $PA/datasets/$DATA-test.csv --stats $OUTFILE --test_out $OUTFILE> "${OUTBASE}${DATA}_${i}"
done