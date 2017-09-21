#!/bin/bash


FILE="$1"
STEP="$2"

touch "out_house__${1}.csv"


for i in $(seq 1 $STEP 30); do
	cat "out_house_${i}_$(($i+$STEP-1))__${1}.csv" >> "out_house__${1}.csv";
done


# cat "out_house_1_10__${1}.csv" >> "out_house__${1}.csv"
# cat "out_house_11_20__${1}.csv" >> "out_house__${1}.csv"
# cat "out_house_21_30__${1}.csv" >> "out_house__${1}.csv"
