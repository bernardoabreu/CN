#!/bin/bash

PA=$HOME'/CN/tp3'
TEST_VERSION="$1"


INPUT_DIR=tests
OUTPUT_DIR=graphs

BASE=$PA/$INPUT_DIR

USE_ALL=true
DIRS=0

DATA_SETS=(yeast_modified)
TYPE=history
LABEL=acc

# parse the options
while getopts 'd:v:l:t:h' opt ; do
  case $opt in
    d) DATA_SETS=("$OPTARG");;
    v) TEST_VERSION=$OPTARG; USE_ALL=false ;;
    t) TYPE=$OPTARG;;
	l) LABEL=$OPTARG;;
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
        mkdir -p $PA/$OUTPUT_DIR/$DATA_SET/$VERSION/
        ARGS="${PA}/${OUTPUT_DIR}/${DATA_SET}/${VERSION}/out"
        TYPES=""
        if [ "${TYPE}" = "history" ]; then
            while read -r TEST_TYPE ; do

    			# mkdir -p $PA/$OUTPUT_DIR/$DATA_SET/$VERSION/$TEST_TYPE
    			ARGS=$ARGS" ${BASE}/${DATA_SET}/${VERSION}/${TEST_TYPE}/out_history_${LABEL}"
    			TYPES=$TYPES" $TEST_TYPE"
            	# echo $ARGS
            done <<< "$(ls ${BASE}/${DATA_SET}/${VERSION})"
        elif [ "${TYPE}" = "score" ]; then

            ARGS="${PA}/${OUTPUT_DIR}/${DATA_SET}/${VERSION}/out"
            TYPES=""
            while read -r TEST_TYPE ; do

                # mkdir -p $PA/$OUTPUT_DIR/$DATA_SET/$VERSION/$TEST_TYPE
                ARGS=$ARGS" ${BASE}/${DATA_SET}/${VERSION}/${TEST_TYPE}/out_final_history_${LABEL}"
                TYPES=$TYPES" ${TEST_TYPE}_training"
                # echo $ARGS
            done <<< "$(ls ${BASE}/${DATA_SET}/${VERSION})"

            while read -r TEST_TYPE ; do

                # mkdir -p $PA/$OUTPUT_DIR/$DATA_SET/$VERSION/$TEST_TYPE
                ARGS=$ARGS" ${BASE}/${DATA_SET}/${VERSION}/${TEST_TYPE}/out_score_${LABEL}"
                TYPES=$TYPES" ${TEST_TYPE}_test"
                # echo $ARGS
            done <<< "$(ls ${BASE}/${DATA_SET}/${VERSION})"
        else
            ARGS="${PA}/${OUTPUT_DIR}/${DATA_SET}/${VERSION}/out"
            TYPES=""
            while read -r TEST_TYPE ; do

                # mkdir -p $PA/$OUTPUT_DIR/$DATA_SET/$VERSION/$TEST_TYPE
                ARGS=$ARGS" ${BASE}/${DATA_SET}/${VERSION}/${TEST_TYPE}/out_time"
                TYPES=$TYPES" ${TEST_TYPE}"
                # echo $ARGS
            done <<< "$(ls ${BASE}/${DATA_SET}/${VERSION})"
        fi

        # echo $ARGS

        # DIR=$BASE/$DATA_SET/$VERSION/$TEST_TYPE
        
        # echo $DIR
        # ls $DIR | grep __ | while read -r TEST_OUTPUT ; do
        echo "Processing ${DATA_SET} ${VERSION}"
        # echo "Processing ${LABEL} ${ARGS} ${TYPES}"
        $PA/source/plot.py ${LABEL} $ARGS $TYPES
        # done
    done
done

