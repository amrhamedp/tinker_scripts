#!/usr/local/bin/python
# This script reads in an xyz file and outputs a CAMCASP input file
# Usage: get_cam_input_from_xyz.py <TINKER xyz>

# Note: This script assumes that the xyz files only contain the coordinates.
import sys
import elements as e

__author__ = "Kailong Mao"

def format_num_str(num_str):
	if num_str[0] == "-":
		return num_str[:9] + "00"
	return " " + num_str[:8] + "00"

base_name = sys.argv[1].split(".")[0]

in_file = open(sys.argv[1], "r")
out_file = open(base_name + ".clt", "w")

out_file.write(\
"\
Title {0} : PBE0/AC\n\
\n\
Global\n\
  Units Bohr Degree\n\
  Overwrite Yes\n\
End\n\
\n\
Molecule {0}\n\
  Units Angstrom\n\
".format(base_name))

# This dictionary keeps track of the number of each atom in the molecule,
# so that each atom will be assigned a unique label
num_atoms = {}

line = in_file.readline()
while line != "":
	line = in_file.readline()
	data = line.split()
	if len(data) == 0:
		continue

	# Assign index to identical elements
	if data[1] in num_atoms.keys():
		num_atoms[data[1]] += 1
		atom_label = data[1] + str(num_atoms[data[1]])
	else:
		num_atoms[data[1]] = 0
		atom_label = data[1]


	out_file.write("  " + atom_label.ljust(11) + str(e.ELEMENTS[data[1]].number) + ".0" + \
		" " * 7 + format_num_str(data[2]) + \
		" " * 6 + format_num_str(data[3]) + \
		" " * 6 + format_num_str(data[4]) + \
		"  " + "TYPE " + data[1] + "\n")
out_file.write(
"\
End\n\
\n\
Run-Type\n\
  Properties\n\
  Molecule {0}\n\
  Basis aug-cc-pVTZ\n\
  Aux-basis aug-cc-pVTZ Spherical\n\
  ISA-Aux set2\n\
  File-prefix {0}\n\
  Functional   PBE0\n\
  AC           TH\n\
  Kernel       ALDA+CHF\n\
  SCFcode      DALTON\n\
  #include /Applications/camcasp-5.8/data/camcasp-cmnds/isa-display\n\
End\n\
\n\
Finish\n\
".format(base_name))

out_file.close()
in_file.close()