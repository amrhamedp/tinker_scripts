#!/usr/bin/python2.7
# Author: Kailong Mao
# This script reads in the multipoles from the .key file and updates it using the indices in
# the .xyz file in a way that can be recognized by J. Rackers' modified TINKER program.
# After reading in all the multipoles from the key files, the parameter file is then updated
# Usage: update_multipoles.py <list of key files> <input file> <output file>
import sys
import math
from decimal import Decimal
__author__ = "Kailong Mao"

def get_class_dict(xyz_name):
	"""This function finds the atom class for each atom number in the key file. The result is
	return in a dictionary
	"""
	xyz = open(xyz_name, "r")
	n_atoms = int(xyz.readline().strip())

	class_dict = {}
	for i in range(n_atoms):
		data = xyz.readline().split()
		atom_number = int(data[0])
		class_number = int(data[5])
		class_dict[atom_number] = class_number
	xyz.close()

	return class_dict

def get_atom_class(atom_number, class_dict):
	"""This function finds the corresponding class for each atom using class_dict.
	"""
	key = abs(atom_number)
	atom_class = class_dict[key]
	if atom_number < 0:
		return - atom_class
	return atom_class

def get_multipole_dict(filename):
	"""This function reads in a key file with multipole parameters and returns the result in a
	dictionary whose keys consist of the three atom numbers immediately following the keyword
	'multipole' in the parameter file
	"""
	f = open(filename, "r")

	# First, consume all irrelevant lines
	line = f.readline()
	while "multipole" not in line:
		line = f.readline()

	multipole_dict = {}
	while line.strip() != '':
		data = line.split()
		key = (int(data[1]), int(data[2]), int(data[3]))
		monopole = data[-1]

		dipole = f.readline().strip()
		quadpole1 = f.readline().strip()
		quadpole2 = f.readline().strip()
		quadpole3 = f.readline().strip()
		line = f.readline()
		multipole_dict[key] = [monopole, dipole, quadpole1, quadpole2, quadpole3]

	f.close()
	return multipole_dict

def update_multipole_dict_key(class_dict, multipole_dict):
	"""This function updates the keys in multipole_dict using the mapping found in class_dict
	"""
	new_dict = {}
	for key in multipole_dict.keys():
		new_key = (get_atom_class(key[0], class_dict), \
			       get_atom_class(key[1], class_dict), \
			       get_atom_class(key[2], class_dict))
		new_dict[new_key] = multipole_dict[key]
	return new_dict

def get_file_names(filename):
	"""This function reads in a file containing a list of file names and returns the data in a list
	"""
	f = open(filename, "r")
	l = []

	line = f.readline()
	while line != "":
		if line.strip() != "":
			l.append(line.strip())
		line = f.readline()

	f.close()
	return l

def write_record(key, multipole_dict, outfile):
	"""This function writes a multipole parameter record to output file. The multipole parameter
	record is a value in the multipole dictionary
	"""
	record = multipole_dict[key]
	outfile.write("multipole" + str(key[0]).rjust(6) +  str(key[1]).rjust(5) + str(key[2]).rjust(5) + record[0].rjust(22) + "\n")
	outfile.write(record[1].rjust(69) + "\n")
	outfile.write(record[2].rjust(47) + "\n")
	outfile.write(record[3].rjust(58) + "\n")
	outfile.write(record[4].rjust(69) + "\n")

def update_multipoles(multipole_dict, in_name, out_name):
	"""This function replaces all the multipole parameters in the input file with the parameters
	in the dictionary. The result is written to output file
	"""
	infile = open(in_name, "r")
	outfile = open(out_name, "w")

	line = infile.readline()
	while line != "":
		if "multipole" != line[0:9]:
			outfile.write(line)
		else:
			data = line.split()
			key = (int(data[1]), int(data[2]), int(data[3]))
			if key in multipole_dict.keys():
				write_record(key, multipole_dict, outfile)
				for i in range(4):
					infile.readline()
			else:
				outfile.write(line)
		line = infile.readline()

	outfile.close()
	infile.close()

def main():
	key_files = get_file_names(sys.argv[1])

	complete_multipole_dict = {}
	for i in range(len(key_files)):
		class_dict = get_class_dict(key_files[i].split("_")[0] + ".xyz")
		multipole_dict = get_multipole_dict(key_files[i])
		updated_dict = update_multipole_dict_key(class_dict, multipole_dict)
		complete_multipole_dict.update(updated_dict)

	update_multipoles(complete_multipole_dict, sys.argv[2], sys.argv[3])

main()

	
