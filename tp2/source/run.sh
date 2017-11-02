#!/bin/bash

HOST=$(hostname)

echo $HOST
BASE=$HOME'/CN/tp2'
TEST_VERSION=2
DATA=(SJC1 SJC2 SJC3b)
SUBDIRS=(a1b3)
OUT=tests

ITER=500
ANTS=90
ALPHA=1
BETA=3
DECAY=0.1


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


echo $$ > "${BASE}/norun_${HOST}.pid"


for FILE in ${DATA[*]}; do

    DIR=$BASE/$OUT/$FILE/$TEST_VERSION/

    for SUBDIR in ${SUBDIRS[*]}; do
        mkdir -p "${DIR}${SUBDIR}"

        # ANTS=$SUBDIR

        for i in {1..30}; do
          echo "${FILE} - ${SUBDIR} ${i}"
            $BASE/source/main.py -n $ANTS -i $ITER -a $ALPHA -b $BETA --seed $i -f $BASE/dataset/"${FILE}.dat" --stats "${DIR}${SUBDIR}/out_${FILE}" > "${DIR}${SUBDIR}/${FILE}_${i}"
        done
    done

done

rm "${BASE}/norun_${HOST}.pid"
