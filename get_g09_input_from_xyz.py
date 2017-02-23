#!/usr/local/bin/python
# This script reads in an xyz file and outputs a Gaussian input file
# Usage: get_g09_in.py <TINKER xyz> <Charge>

# Note: This script assumes that the xyz files only contain the coordinates.
import sys

__author__ = "Kailong Mao"

def format_num_str(num_str):
	if num_str[0] == "-":
		return num_str[:9]
	return " " + num_str[:8]

base_name = sys.argv[1].split(".")[0]

in_file = open(sys.argv[1], "r")
out_file = open("g09_input/" + base_name + ".com", "w")

out_file.write("%Mem=2000MB\n")
out_file.write("%Chk={0}.chk\n\n".format(base_name))
out_file.write("#MP2/aug-cc-pVTZ Density=MP2\n\n")
out_file.write(base_name + " at MP2/aug-cc-pVTZ\n\n")
out_file.write(sys.argv[2] + " 1\n")

line = in_file.readline()
while line != "":
	line = in_file.readline()
	data = line.split()
	if len(data) == 0:
		continue
	out_file.write(data[1] + " " * 5 + format_num_str(data[2]) + \
		                     " " * 3 + format_num_str(data[3]) + \
		                     " " * 3 + format_num_str(data[4]) + "\n")
out_file.write("\n")

out_file.close()
in_file.close()