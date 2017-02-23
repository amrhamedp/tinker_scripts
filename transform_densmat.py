#!/usr/bin/python2.7
# Author: Kailong Mao
# This script takes as input both an NWCHEM .movecs orbital file and .fchk file.
# It first determines the transformation between the orbital coefficients in the
# two files, and then transforms the density matrix in the .fchk file based on
# the transformation of the orbitals.
# Usage: transform_densmat.py <.movecs> <.fchk> <orbital_configuration>
import sys
import math
import numpy as np
from decimal import Decimal
__author__ = "Kailong Mao"

def is_equal(s1, s2):
	"""This function returns true if the two numbers represented in scientic notation
	are roughly equal. Otherwise, it returns false. They are considered equal if
	1) s1 and s2 share the first four significant digits and they have the same exponents; or
	2) they are both very small numbers
	"""
	sig1 = s1[0:3]
	sig2 = s2[0:3]
	exp1 = int(s1.split("E")[1])
	exp2 = int(s2.split("E")[1])

	if sig1 == sig2 and exp1 == exp2:
		return True
	return False

def get_sci_notation(l):
	"""This function converts every string in the input list to its corresponding scientific 
	notation
	"""
	newL = []
	for i in l:
		newL.append('%.3E' % Decimal(i))
	return newL


def read_movecs(filename, orbital_num):
	"""This function reads in the coefficients of the first orbital in the movecs file
	and returns them in a list
	"""
	coeffs = []
	movecs = open(filename, "r")

	# First, consume all lines until the first orbital is encountered
	line = movecs.readline()
	while ("MO " + str(orbital_num)) not in line:
		line = movecs.readline()

	# Next, read in the coefficients
	line = movecs.readline()
	while (("MO " + str(orbital_num + 1)) not in line) and (line != ""):
		coeffs += line.split()
		line = movecs.readline()

	movecs.close()
	return get_sci_notation(coeffs)

def read_fchk_coeffs(filename, orbital_num):
	"""This function reads in the coefficients of the first orbital in the fchk file produced by
	psi4 and returns them in a list
	"""
	coeffs = []
	fchk = open(filename, "r")

	# First, consume all lines until alpha coefficients are reached
	line = fchk.readline()
	while "Alpha MO coefficients" not in line:
		line = fchk.readline()

	nCoeffs = int(round(int(line.split()[-1]) ** 0.5))
	nLines = int(math.ceil(nCoeffs * orbital_num / 5.0))
	for i in range(nLines):
		line = fchk.readline()
		coeffs += line.split()	
	fchk.close()

	return get_sci_notation(coeffs[(orbital_num - 1) * nCoeffs : orbital_num * nCoeffs])

def read_fchk_densmat(filename, dtype):
	"""This file reads in the density matrix from the fchk file and returns it in a list
	"""
	densities = []
	infile = open(filename, "r")

	line = infile.readline()
	while("Total " + dtype + " Density") not in line:
		line = infile.readline()

	total_lines = int(math.ceil(float(line.split()[-1]) / 5.0))
	for i in range(total_lines):
		densities += infile.readline().split()
	infile.close()
	return densities

def get_boundaries(i, orbital_types):
	"""This function defines the search boundaries for each mapping search
	"""
	t = orbital_types[i]
	left = i
	right = i

	while left >= 0 and orbital_types[left] == t:
		left -= 1

	while right < len(orbital_types) and orbital_types[right] == t:
		right += 1

	return left + 1, right

def get_mapping(l1, l2, orbital_types):
	"""This function finds where each value in l1 occurs in l2. It returns a list that stores
	the indices of the corresponding elements in l2 for the elements in l1
	"""
	mapping = [-1] * len(l1)
	for i in range(len(l1)):

		left, right = get_boundaries(i, orbital_types)

		if l1[i] != "0.000E+00":
			# Search is restricted to the neighoring elements
			for j in range(left, right):
				if is_equal(l2[j], l1[i]):
					mapping[i] = j
					break
	return mapping

def transform_densmat(old_mat_array, mapping):
	"""This function transforms the old density matrix into a new density matrix based on the 
	mapping
	"""
	n = len(mapping)

	# Intialize the matrices
	new_mat = []
	old_mat = []
	for i in range(n):
		new_row = []
		for j in range(n):
			new_row.append("")
		old_mat.append(new_row)
		new_mat.append(new_row[:])

	# First, reconstruct the old density matrix based on the input from fchk file
	temp_array = old_mat_array[:]
	for i in range(n):
		for j in range(0, i+1):
			val = temp_array.pop(0)
			old_mat[i][j] = val
			old_mat[j][i] = val

	for i in range(n):
		for j in range(i, n):
			new_i = mapping[i]
			new_j = mapping[j]
			new_mat[new_i][new_j] = old_mat[i][j]
			new_mat[new_j][new_i] = old_mat[j][i]
	return new_mat

def write_densmat(mat):
	"""This function writes out the upper triangle of the density matrix to a flattened file,
	which is then read by CamCasp in downstream calculations
	"""
	n = len(mat)
	outfile = open(sys.argv[2].split(".")[0] + ".den", "w")

	for i in range(n):
		for j in range(n):
			outfile.write(mat[i][j] + "\n")
	outfile.close()

def flip_sign(l):
	"""This function flips the signs of all numbers in the input list
	"""
	for i in range(len(l)):
		if l[i][0] == "-":
			l[i] = l[i][1:]
		else:
			l[i] = "-" + l[i]

def mask_zeros(l):
	"""This function replaces values with extremely small exponents and values of negative
	zero with "0.000E+00"
	"""
	for i in range(len(l)):
		if l[i] == "-0.000E+00" or int(l[i].split("E")[1]) < -8:
			l[i] = "0.000E+00"

def read_orbital_config(filename):
	"""This function reads in an orbital configuration file. It must be of the following format:
	1) First line: The atoms in the molecule (for example, O H H)
	2) Following lines should be the basis set format for each atom (for example, O:3s2p1d)
	It returns a list, each element in which corresponds to the type of orbital at the given location
	"""
	orbital_config = {}
	infile = open(filename, "r")
	atoms = infile.readline().split()

	line = infile.readline()
	while line != "":
		data = line.split(":")
		orbital_config[data[0].strip()] = data[1].strip()
		line = infile.readline()

	infile.close()

	orbital_types = []
	for atom in atoms:
		config = orbital_config[atom]
		for i in range(0, len(config), 2):
			n = int(config[i])
			t = config[i+1]

			for j in range(n):
				if t == "s":
					orbital_types.append(t + str(j))
				elif t == "p":
					orbital_types += [t + str(j)] * 3
				elif t == "d":
					orbital_types += [t + str(j)] * 5

	return orbital_types

def fix_missing(mapping, orbital_types):
	"""For each orbital type s, p, d, if only one component in the mapping is flagged -1 (missing), then
	this function infers the correct mapping for that component based on the mappings of all the other 
	components of the same orbital
	"""
	for i in range(len(mapping)):
		if mapping[i] == -1:
			left, right = get_boundaries(i, orbital_types)

			# First, check if there is only one component missing. If not, we cannot fix the mapping
			count = 0
			for j in mapping[left : right]:
				if j == -1:
					count += 1
			if count > 1:
				break

			# Next, find the missing element:
			for k in range(left, right):
				if k not in mapping[left : right]:
					mapping[i] = k
					break


def merge_mapping(final_mapping, m):
	"""This function merges two mappings. Specifically, it fills the gap in final_mapping with
	information from m
	"""
	for i in range(len(final_mapping)):
		if final_mapping[i] == -1 and m[i] != -1:
			final_mapping[i] = m[i]

def get_density_matrix(m, nocc):
	transformed_m = np.array([map(np.float, i) for i in m])
	return 2.0 * np.dot(np.transpose(transformed_m[0:nocc]), transformed_m[0:nocc])

def main():
	orbital_types = read_orbital_config(sys.argv[3])
	n_orbitals = len(orbital_types)

	movecs_coeffs_m = []
	fchk_coeff_m = []

	final_mapping = [-1] * n_orbitals
	for i in range(1, n_orbitals + 1):
		movecs_coeffs = read_movecs(sys.argv[1], i)
		fchk_coeffs = read_fchk_coeffs(sys.argv[2], i)

		movecs_coeffs_m.append(movecs_coeffs)
		fchk_coeff_m.append(fchk_coeffs)

		if not is_equal(fchk_coeffs[0], movecs_coeffs[0]):
			flip_sign(fchk_coeffs)
		mask_zeros(movecs_coeffs)
		mask_zeros(fchk_coeffs)

		mapping = get_mapping(fchk_coeffs, movecs_coeffs, orbital_types)
		merge_mapping(final_mapping, mapping)
		
	fix_missing(final_mapping, orbital_types)

	print get_density_matrix(movecs_coeffs_m, 5)[0]
	print get_density_matrix(fchk_coeff_m, 5)[0]

	print "Final mapping:"
	print final_mapping
	old_densmat_array = read_fchk_densmat(sys.argv[2], "SCF")
	
	new_mat = transform_densmat(old_densmat_array, final_mapping)

	for i in range(len(final_mapping)):
		for j in range(len(final_mapping)):
			if new_mat[i][j] == "":
				print i, j, final_mapping.index(i), final_mapping[j]
	write_densmat(new_mat)
main()

	
