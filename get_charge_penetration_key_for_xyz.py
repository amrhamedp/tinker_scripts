#!/usr/local/bin/python
# This script creates a TINKER POTENTIAL key file for J. Rackers' version of
# POTENTIAL with charge penetration
# Usage: get_charge_penetration_key_for_xyz.py <xyz file>
import sys

__author__ = "Kailong Mao"
base_name = sys.argv[1].split(".")[0]

cp_data = {1 : [404,402,406,408,41,410,411,68,109, \
                155,415,421,445,449,446,533,529,537,538,545,546,547, \
                465,468,471,498,501,504,507], \
           2 : [2,430,438,107,419,442,39,66,151,514,521,558, \
                454,458,462,526,539,548,508], \
           3 : [218,424,426,428,434,436,515,516,517,522, \
                523,559,560,561,562,563,564,477,478,479,485,486,487, \
                493,494,495], \
           4 : [451,455,459], \
           5 : [448], \
           6 : [470,492,503], \
           7 : [108,40,67,154,401,413,412,407,409,405,414, \
                420,506,527,534,535,531,443,447,463,466,469,496,499,502],\
           8 : [104,152,403,416,524,528], \
           9 : [217,423,425,427,431,433,435,439,509,510,512, \
                518,519,540,541,542,543,549,550,551,552,553,554,556,557, \
                472,473,474,475,480,481,482,483,488,489,490,491], \
           10 : [532,444], \
           11 : [467,484,500], \
           12 : [106,418,525], \
           13 : [422,429,437,511,513,520,555], \
           14 : [65,505,536], \
           15 : [1,150,441,38,544,452,456,460], \
           16 : [464,476,497], \
           17 : [432,440], \
           18 : [105,153,417,530,450,453,457,461]}

def find_class(atom_type):
    """This function finds the corresponding CPC class for each atom type
    """
    for i in cp_data.keys():
        if atom_type in cp_data[i]:
            return i

in_file = open(sys.argv[1], "r")
out_file = open(base_name + ".cp", "w")

out_file.write("PENETRATION           GORDON\n")

line = in_file.readline()
line = in_file.readline()
while line != "":
    data = line.split()
    atom_index = data[0]
    atom_type = data[5]
    atom_class = str(find_class(int(atom_type)))
    out_file.write("CPCLASS" + atom_index.rjust(5) + atom_class.rjust(7) + "\n")
    line = in_file.readline()

in_file.close()
out_file.close()