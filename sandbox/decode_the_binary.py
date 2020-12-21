
""" Spliiting the chromosome into the problem variables per the specified bit size"""

import random

VAR_NUM_BITS=5
NUM_VARS=2
NUM_GENES=VAR_NUM_BITS*NUM_VARS

chromosome=[random.randint(0,1) for i in range(NUM_GENES)]   #[0, 1, 0, 1, 0, 0, 1, 1]

print(f'chromosome: {chromosome}')



var_list=[]
var=[]
a=0
b=1
for i in range(NUM_VARS):

    var=chromosome[a:(VAR_NUM_BITS*b)]
    var_list.append(var)
    print(f'variable {b}------>{var}')
    
    a+=VAR_NUM_BITS
    b+=1
    

print(var_list)




