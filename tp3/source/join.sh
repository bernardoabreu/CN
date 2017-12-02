#!/bin/bash


FILE="$1"
BASE="$2"

touch "out_yeast_modified__${1}.csv"


for i in $(seq 1 30); do
	cat "${2}/out_yeast_modified_${i}__${1}.csv" >> "out_yeast_modified__${1}.csv";
done


# cat "out_house_1_10__${1}.csv" >> "out_house__${1}.csv"
# cat "out_house_11_20__${1}.csv" >> "out_house__${1}.csv"
# cat "out_house_21_30__${1}.csv" >> "out_house__${1}.csv"
