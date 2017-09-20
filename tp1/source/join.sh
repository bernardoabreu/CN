#!/bin/bash


FILE="$1"

touch "out_house__${1}.csv"

cat "out_house_1_10__${1}.csv" >> "out_house__${1}.csv"
cat "out_house_11_20__${1}.csv" >> "out_house__${1}.csv"
cat "out_house_21_30__${1}.csv" >> "out_house__${1}.csv"
