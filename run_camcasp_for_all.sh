#!/bin/bash
# This script converts all xyz files to CAMCASP output files,
# runs CAMCASP and gets ISA and DMA multipoles for all molecules
# in the directory
# Author: Kailong Mao

for i in $(ls *.xyz)
do
	base_name="${i%.*}"
	python ~/Desktop/scripts/get_cam_input_from_xyz.py $i
	runcamcasp.py --direct --nproc 4 -q bg $base_name
done