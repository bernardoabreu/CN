#!/bin/bash

DATA_SET=house


for i in {1..30}; do
	$HOME/CN/tp1/source/gen.py "${DATA_SET}_${i}" $DATA_SET
done