#!/bin/bash

# This script adds the missing atom info to the fitted multipole 
# parameter file from POTENTIAL

for i in *.key
do
	if ! [ -e ${i}_fitted ]
	then
		echo "Missing ${i}_fitted"
		continue
	fi

	cat $i | grep "atom" && cat ${i}_fitted > ${i}_fitted
done
