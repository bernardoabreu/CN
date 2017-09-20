#!/bin/bash

ls | grep __ | while read -r line ; do
    echo "Processing $line"
    # your code goes here
done