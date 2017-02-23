#!/bin/bash
# This program runs g09 on all the Gaussian input files in a given directory and outputs
# the .chk files needed for downstream processing
# Author: Kailong Mao

# Usage: get_all_fchk.sh <directory path>

# Step 1: Run g09 and get the checkpoint file
for i in ${1}*.com
do
	base_name="${i%.*}"
	g09 $i > ${base_name}.out
done