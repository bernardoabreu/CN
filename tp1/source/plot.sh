#!/bin/bash

PA=$HOME'/CN/tp1'
TEST_VERSION="$1"

BASE=$PA/tests

USE_ALL=true
DIRS=0

DATA_SETS=(keijzer-7 keijzer-10 house)


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
        TEST_VERSION=(`ls $PA/tests/$DATA_SET`)
    fi

    for VERSION in ${TEST_VERSION[*]}; do

        ls $PA/tests/$DATA_SET/$VERSION | while read -r TEST_TYPE ; do

            mkdir -p $PA/graphs/$DATA_SET/$VERSION/$TEST_TYPE
            DIR=$PA/tests/$DATA_SET/$VERSION/$TEST_TYPE
            
            echo $DIR
            ls $DIR | grep __ | while read -r TEST_OUTPUT ; do
                echo "Processing $TEST_OUTPUT"
                $PA/source/plot.py $DIR/$TEST_OUTPUT $PA/graphs/$DATA_SET/$VERSION/$TEST_TYPE
            done
        done
    done
done
