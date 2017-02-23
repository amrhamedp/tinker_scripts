# This script was written to process the CPCLASS data from J. Rackers
# It outputs a tinker key file with the CPCLASS for eah atom in the xyz file

# Update #1: Added all the ALPHA-PERM parameters to get JR's version of
# POTENTIAL to work properly

__author__ = "Kailong Mao"

data = {1 : [404,402,406,408,41,410,411,68,109, \
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

out_file = open("cpcclass.key", "w")
for i in data.keys():
	for j in data[i]:
		out_file.write("CPCLASS" + str(j).rjust(5) + str(i).rjust(7) + "\n")
out_file.write(
"\n\n\
ALPHA-PERM     1     3.2484\n\
ALPHA-PERM     2     3.2632\n\
ALPHA-PERM     3     3.4437\n\
ALPHA-PERM     4     2.7476\n\
ALPHA-PERM     5     2.6247\n\
ALPHA-PERM     6     3.6696\n\
ALPHA-PERM     7     3.5898\n\
ALPHA-PERM     8     3.1286\n\
ALPHA-PERM     9     3.2057\n\
ALPHA-PERM     10     3.3112\n\
ALPHA-PERM     11     3.4749\n\
ALPHA-PERM     12     3.7071\n\
ALPHA-PERM     13     3.6358\n\
ALPHA-PERM     14     4.0135\n\
ALPHA-PERM     15     4.1615\n\
ALPHA-PERM     16     4.4675\n\
ALPHA-PERM     17     4.3778\n\
ALPHA-PERM     18     3.7321\n\
")
out_file.close()