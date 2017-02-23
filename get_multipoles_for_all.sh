#!/bin/bash
# This script reads a CAMCASP output and converts all ISA and DMA multipoles
# to TINKER format
# Author: Kailong Mao

for i in $(cat ../molecules.data)
do
	base_name=$i
	cp ${base_name}/OUT/${base_name}.out .

	# Clean up, convert CAMCASP output to GDMA output
	# rm -r ${base_name}
	python ~/Desktop/scripts/read_camcasp.py ${base_name}.out
	# rm ${base_name}.out
	# rm ${base_name}.clt

	# Convert all the ISA and DMA multipoles to TINKER format
	for j in $(ls ${base_name}*.multipoles)
	do
		poledit 1 $j 0 0 0 N N 
		# rm $j
	done
done