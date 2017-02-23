#!/bin/bash
# This script converts all xyz files in the current directory to g09 input files
# Usage: convert_all_xyz_to_g09.sh <charges>
      
# Make "new line" the only separator
IFS=$'\n' 

# Make a new directory to store all g09 input files
mkdir g09_input

for j in $(cat $1)    
do
	IFS=$' ' 
	read xyz charge <<< $j
    python ~/Desktop/scripts/get_g09_input_from_xyz.py $xyz $charge
    IFS=$'\n' 
done