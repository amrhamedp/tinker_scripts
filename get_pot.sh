#!/bin/bash
# This program implements the protocol in "Polarizable Atomic Multipole-Based 
# Molecular Mechanics for Organic Molecules" by P. Ren
# It assumes that the environmental variables have been set up properly.
# See setup.sh in the same directory
# Author: Kailong Mao

# Usage: get_pot.sh

# Step 1: Run g09, get the checkpoint file, and convert it to correct format
modified_p="/user/jrackers/tinker-git/bin/potential-git"
near_grid_key="/user/mao/Desktop/scripts/near_grid.key"
fitting_key="/user/mao/Desktop/scripts/fitting.key"
charge_penetration_key="/user/mao/Desktop/scripts/charge_penetration.key"

for i in *.xyz
do
	base_name="${i%.*}"

	# Step 2: Generate the .pot file
	# Try to generate the grid using DMA multipoles later on and see what happens

	if ! [ -e ${base_name}_isa.key ] || [ -e ${base_name}_far.pot ]
	then
		continue
	fi

	# First, get the .pot file for the far grid
	potential 1 $i ${base_name}_dma_1.key  
	cubegen 0 potential=MP2 ${base_name}.fchk ${base_name}.cube -5 h < ${base_name}.grid
	sleep 1
	rm ${base_name}.grid
	potential 2 ${base_name}.cube
	rm ${base_name}.cube
	mv ${base_name}.pot ${base_name}_far.pot

	# Next, get the .pot file for the near grid
	potential -k $near_grid_key 1 $i ${base_name}_dma_1.key  
	cubegen 0 potential=MP2 ${base_name}.fchk ${base_name}.cube -5 h < ${base_name}.grid
	sleep 1
	rm ${base_name}.grid
	potential 2 ${base_name}.cube
	rm ${base_name}.cube
	mv ${base_name}.pot ${base_name}_near.pot

done