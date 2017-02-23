#!/usr/bin/python2.7
# Author: Kailong Mao
# This script reads in two square matrices from file and determines how one matrix is transformed
# into the other
# Usage: match_matrices.py <matrix 1> <matrix 2>
import sys
import math
from decimal import Decimal
__author__ = "Kailong Mao"

def is_equal(s1, s2):
	"""This function returns true if the two numbers represented in scientic notation
	are roughly equal. Otherwise, it returns false. They are considered equal if
	1) s1 and s2 share the first four significant digits and they have the same exponents; or
	2) they are both very small numbers
	"""
	sig1 = s1[0:4]
	sig2 = s2[0:4]
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

def mask_zeros(l):
	"""This function replaces values with extremely small exponents and values of negative
	zero with "0.000E+00"
	"""
	for i in range(len(l)):
		if l[i] == "-0.000E+00" or int(l[i].split("E")[1]) < -8:
			l[i] = "0.000E+00"

def read_file(filename):
	""" This function reads in a file with a square matrix and returns a square matrix
	"""
	f = open(filename)
	flat_list = []

	line = f.readline()
	while line != "":
		new_list = get_sci_notation(line.split())
		mask_zeros(new_list)
		flat_list += new_list
		line = f.readline()

	dim = int(round(len(flat_list) ** 0.5))
	matrix = []
	for i in range(dim):
		new_row = []
		for j in range(dim):
			new_row.append(flat_list.pop(0))
		matrix.append(new_row)
	f.close()

	return matrix

def find_mapping(m1, m2, coords):
	""" For the element in row coords[0] and column coords[2] in matrix 1, find the 
	corresponding element in matrix 2
	"""
	matches = []
	for i in range(len(m2)):
		for j in range(len(m2[0])):
			if is_equal(m1[coords[0]][coords[1]], m2[i][j]):
				matches.append([i, j])
	return matches

def main():
	m1 = read_file(sys.argv[1])
	m2 = read_file(sys.argv[2])

	for i in range(len(m1)):
		for j in range(i, len(m1[0])):
			if m1[i][j] != "0.000E+00":
				matches = find_mapping(m1, m2, [i, j])
				if len(matches) < 3:
					print [i, j], "=>", matches
main()

	
