#!/bin/bash

BASE=$HOME'/CN/tp3'
TEST_VERSION=1
DATA=('yeast_modified')
SUBDIRS=(500)
OUT=tests2


NEURONS=16
HIDDEN_LAYERS=1
EPOCHS=500
LEARNING_RATE=0.1
BATCH_SIZE=32
LR_DECAY=0.0




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


START="$1"
END="$2"

echo $$ > "${BASE}/norun_${HOST}.pid"


for FILE in ${DATA[*]}; do

    DIR=$BASE/$OUT/$FILE/$TEST_VERSION/

    for SUBDIR in ${SUBDIRS[*]}; do
        mkdir -p "${DIR}${SUBDIR}"

        LR_DECAY=$SUBDIR

        for i in $(seq $START $END); do
          echo "${FILE} - ${SUBDIR} ${i}"
          $BASE/source/main.py -n $NEURONS -hl $HIDDEN_LAYERS -e $EPOCHS -lr $LEARNING_RATE -b $BATCH_SIZE -d $LR_DECAY -s $i -f $BASE/dataset/"${FILE}.csv" --stats "${DIR}${SUBDIR}/out_${FILE}_${i}" > "${DIR}${SUBDIR}/${FILE}_${i}"
        done
    done
done

