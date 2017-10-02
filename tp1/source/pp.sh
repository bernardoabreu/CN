#!/bin/bash


PA=$HOME'/CN/tp1'


TEST_VERSION="$1"
TYPE="$2"
DATA="$3"

OUTFILE="out_${DATA}__${TYPE}.csv"
BASE=$PA/tests2/$DATA/$TEST_VERSION

# $PA/source/plot.py $TYPE $DATA $BASE/50/$OUTFILE $BASE/100/$OUTFILE $BASE/500/$OUTFILE
# 
# $PA/source/plot.py $TYPE $DATA $BASE/500/$OUTFILE
# 
$PA/source/plot.py $TYPE $DATA $PA/tests2/$DATA/2/100/$OUTFILE $BASE/mut_high/$OUTFILE
# 
# 
# $PA/source/plot.py $TYPE $DATA $BASE/3/$OUTFILE $BASE/7/$OUTFILE

# $PA/source/plot.py $TYPE $DATA $BASE/3/$OUTFILE $PA/tests2/$DATA/4/3/$OUTFILE
# 
# $PA/source/plot.py $TYPE $DATA $PA/tests2/$DATA/4/7/$OUTFILE $BASE/0/$OUTFILE
