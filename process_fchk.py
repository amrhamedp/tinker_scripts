#!/usr/bin/python2.7
# Author: Kailong Mao
# This script extracts the MP2 densities from an fchk file and puts the numbers in a file, one number per line
# so that molecular_orbitals.F90 can read it
# Usage: process_fchk.py <density type> <fchk file>
import sys
__author__ = "Kailong Mao"

density = sys.argv[1]
fchk = sys.argv[2]

infile = open(fchk, "r")
outfile = open(fchk.split(".")[0] + ".den", "w")

line = infile.readline()
while("Total " + density + " Density") not in line:
	line = infile.readline()

total_lines = int(line.split()[-1])/5
for i in range(total_lines):
	values = infile.readline().split()
	for j in values:
		outfile.write(j+"\n")

infile.close()
outfile.close()