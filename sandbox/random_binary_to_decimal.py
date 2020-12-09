
import random
import math

XMIN=5
XMAX=30
VARIABLE_NAME='Radius'
NUM_BITS=4

def random_binary(n):
    a=[random.randint(0,1) for i in range(n)]
    print(a)

    prepare_conversion(a)
    

def prepare_conversion(a):
    g=''
    for i in range(0,len(a)):
            g=g+str(a[i])
            print(f'{g}----->{i}')
    print(g)

    convert(g)

    

def convert(g):
    d=int(g,2)

    print(f'Decimal Value: {d}')

    decision_variables(d)

    
def decision_variables(d,xmin=XMIN,xmax=XMAX):

    x=xmin+((xmax-xmin)/((2**NUM_BITS)-1))*d

    print(f'Scaled Decision Variable ({VARIABLE_NAME}): {round(x,2)}')

def precision():

    p=(XMAX-XMIN)/(2**NUM_BITS-1)
    return round(p,2)


# ----------MAIN----------MAIN

print(f'{VARIABLE_NAME} Bounds\n:Min Value:{XMIN}\nMax Value:{XMAX}')
print(f'\nBit Length:{NUM_BITS}\nPrecision:{precision()}')

random_binary(NUM_BITS)
