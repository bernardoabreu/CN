#!/bin/bash

PA=$HOME'/CN/tp2'
TEST_VERSION="$1"


INPUT_DIR=tests

BASE=$PA/$INPUT_DIR

USE_ALL=true
DIRS=0

DATA_SETS=(SJC1 SJC2 SJC3b)


# parse the options
while getopts 'd:v:h' opt ; do
  case $opt in
    d) DATA_SETS=("$OPTARG");;
    v) TEST_VERSION=$OPTARG; USE_ALL=false ;;
    h) echo "Options: -d data sets (default: ${DATA_SETS[*]})"
       echo "         -v test version (default: Use all)";
       exit 0 ;;
  esac
done

# skip over the processed options
shift $((OPTIND-1)) 


for DATA_SET in ${DATA_SETS[*]}; do

    if $USE_ALL; then
        TEST_VERSION=(`ls ${PA}/${INPUT_DIR}/${DATA_SET}`)
    fi

    for VERSION in ${TEST_VERSION[*]}; do

        ls $BASE/$DATA_SET/$VERSION | while read -r TEST_TYPE ; do

            DIR=$BASE/$DATA_SET/$VERSION/$TEST_TYPE
            
            echo $DIR
            ls $DIR | grep __ | while read -r TEST_OUTPUT ; do
                echo "Processing $TEST_OUTPUT"
                python $PA/source/fixbest.py $PA/$INPUT_DIR/$DATA_SET/$VERSION/$TEST_TYPE/"out_${DATA_SET}__best.csv"
            done
        done
    done
done
