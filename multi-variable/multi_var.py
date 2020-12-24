"""My attempt to build a genetic algorithm from scratch to solve the onemax problem"""

# %%
import random
import pprint
import matplotlib.pyplot as plt
import sys
import math
import numpy as np

## Constants

VAR_NUM_BITS=8
NUM_VARS=6
NUM_GENES=NUM_BITS=VAR_NUM_BITS*NUM_VARS
POP_SIZE=50
P_MUTATION=.05
P_CROSSOVER=.7
GEN_COUNT=20
OUTPUT_FILE_LIMIT=100
XMIN=[30,25,180,2850,550,600]
XMAX=[700,500,2500,4000,1650,1200]
VARIABLE_NAME='TBD'
OPTIMIZATION='max'  #Option----> 'max'

Variable_avg=[]
values_list=[]

INDEX_TO_STUDY=0


# %%
class Individuals():
    """Random generated Binary chromosomes. Each chromsome has 10 genes."""
    def __init__(self):
        self.ind=[]

    def make_individual(self):
        i=[random.randint(0,1) for i in range(NUM_GENES)]
        return i

        # print(i)

# %%
class Population():

    def __init__(self):
        self.a=Individuals()
        self.the_population=[]
        self.make_population()

    def make_population(self):
        for i in range(POP_SIZE):
            self.the_population.append(self.a.make_individual())

        print(self.the_population)
    
        return self.the_population


    
# %%

def fitness_score(x):
    """returning the fitness score"""
    global scaled_var_list
    var_list=vars_from_chromo(x)
    scaled_var_list=[]
    variable_study=[]
    c=1

    avg=lambda z: sum(z)/len(z)
    
    for index,v in enumerate(var_list):
        #---->coverting the binary list to binary string
        g=''
        for i in range(0,len(v)):
                g=g+str(v[i])
                # print(f'{g}----->{i}')
        print(g)

        d=int(g,2) #------------> Decimal Value (DV)
        print(f'Decimal Value: {d}')

        xmin=XMIN[index]
        xmax=XMAX[index]
        variable_name=c
        t=xmin+((xmax-xmin)/((2**VAR_NUM_BITS)-1))*d  #------>ACTUAL VALUE
        print(f'Scaled Decision Variable ({c}): {round(t,2)}')
        scaled_var_list.append(t)
        c+=1

        var_to_study=INDEX_TO_STUDY   # specify the index for the item to study
        if index==var_to_study:
            variable_study.append(t)
            # Variable_avg.append(t)

    ## Capture variable to study variable trends
    Variable_avg.append(avg(variable_study))
    # print(f'Variable Average: {Variable_avg}')
    values_list.append(scaled_var_list)

    ## Scenerio: Find the min or max value of y=f(x) over the range of [XMIN,XMAX]
   

    TARGET=sum(XMAX[0:NUM_VARS])
    y = sum(scaled_var_list)

    if OPTIMIZATION=='max':
        discret_spend=scaled_var_list[5]/y
        criteria=any([y>TARGET,(scaled_var_list[0]+scaled_var_list[1]>500),discret_spend>.025])
        if criteria:
            y=0
        # if y>TARGET :
        #     y=0
    elif(OPTIMIZATION=='min'):
        y=abs(TARGET-y)
        # criteria=any([y>TARGET])
        # if criteria:
        #     y=abs(TARGET-y)

    
    return y

def vars_from_chromo(x):
    """Breakdown the binary genome into the problem variables (binary). All varibles with the same number of bits."""

     
    chromosome=x
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
    return var_list


# %%


def populationSum(fitness):
    """for the area of circle problem"""
    
    s=sum(fitness)
    avg=s/len(fitness)
    print(f'\nPopulation average: {avg}\n')
    send_results_to_file({'Population average':avg},'a')
    return avg


# %%

def roulette_weights(fitness):
    
    s=sum(fitness)

    # w=[round((i/s),2)*100 for i in fitness]
    w=[i for i in range(len(fitness))]
    # print(f'Relative Portion: {w}')
    return w

def roulette_selection():
    pass


def tornament_select(gen_stat,pool_size=POP_SIZE,k=2):
    """Perform Tornament Selection and populate the mating pool"""

    t_check=[]
    mating_pool=[]

    # initialize tornament counter
    c=0 
    
    while len(mating_pool)<POP_SIZE:
        tornament=[gen_stat[random.randint(0,len(gen_stat)-1)] for i in range(k)]

        b=(tornament[0][3],tornament[1][3])
        if (b[0]==b[1]):
            continue

        if len(t_check)>0:
            
            check_repeats=[b[0] in i and b[1] in i for i in t_check]

            print(f't-check:\n{t_check}')
            print(f'\ncheck for repeats:\n{check_repeats}')

            send_results_to_file({'t-check':t_check},'a')
            send_results_to_file({'check for repeats':check_repeats},'a')
           
            if not any(check_repeats) and not (b[0]==b[1]):
                if (OPTIMIZATION=='max'):
                    mating_pool.append(max(tornament))
                elif(OPTIMIZATION=='min'):
                    mating_pool.append(min(tornament))

                t_check.append(b)

        else:
            if (OPTIMIZATION=='max'):
                mating_pool.append(max(tornament))
            elif(OPTIMIZATION=='min'):
                mating_pool.append(min(tornament))
            t_check.append(b)

        
        c=c+1

        if c==500:
            print(f't-check limit exceeds the specified {c}')
            exit()

        print(f'tornament number: {c}')
        print(f'tornament selection:')
        pprint.pprint(tornament)
        send_results_to_file({'tornament number':c},'a')
        send_results_to_file({'tornament selection':tornament},'a')

    print(f'tornament selection: {tornament}\n')
    print(f'tornament index check: {t_check}\n')

    send_results_to_file({'mating pool':mating_pool},'a')
    return mating_pool


def single_point_crossover(mating_pool,k=2):

    send_results_to_file({'Mating Process':'SINGLE POINT CROSSOVER'},'a')
    # Input: mating_pool
    print(f'MATING POOL\n')
    pprint.pprint(mating_pool)

    d=0
    # Initialize the offspring list
    offspring=[]

    while len(offspring)<POP_SIZE:
       
        # Randomly Choose 2 binary strings (chromosones) from the mating pool
        parents=[mating_pool[random.randint(0,len(mating_pool)-1)] for i in range(k)]
        print(f'\nparents:\n{parents}')
        send_results_to_file({'PARENTS':parents},'a')
        
        if parents[0][3]==parents[1][3]:
            d=d+1
            if d>100:
                exit()
            else:
                continue

        # Crossover of two parents occurs with propability (pb)
        cross_prob=random.random()
        print(f'\ncrossover probability: {cross_prob}')
        send_results_to_file({'crossover probability':cross_prob},'a')

        if cross_prob<P_CROSSOVER:
            cross_site=random.randint(0,NUM_GENES-1)
            print(f'crossover site: {cross_site}')
            send_results_to_file({'crossover site':cross_site},'a')

            # Perform the crossover if crossover probability is met.
            P1=parents[0][1]
            P2=parents[1][1]

            print(f'\nBEFORE CROSSOVER\nParent-1:{(P1,parents[0][3])}\nParent-2:{(P2,parents[1][3])}')
            send_results_to_file({'BEFORE CROSSOVER':{'Parent-1':(P1,parents[0][3]),'Parent-2':(P2,parents[1][3])}},'a')
            a=P1[cross_site:]
            b=P2[cross_site:]

            P1[cross_site:]=b
            P2[cross_site:]=a

            print(f'\nAFTER CROSSOVER\nOffspring-1:{(P1,parents[0][3])}\nOffspring-2:{(P2,parents[1][3])}')
            send_results_to_file({'AFTER CROSSOVER':{'Offspring-1':(P1,parents[0][3]),'Offspring-2':(P2,parents[1][3])}},'a')
            print(f'Ready for Offpring list:\n{parents}')
            send_results_to_file({'Ready for Offpring list':parents},'a')

            # Append the new borns to the offspring list
            # for i in parents:
            #     offspring.append(i)

            c=[offspring.append(i) for i in parents]
            print(f'\nOFFSPRING LIST:')
            pprint.pprint(offspring)
            send_results_to_file({'OFFSPRING LIST':offspring},'a')

        else:
            # Append the elite parrents to the offspring list
            c=[offspring.append(i) for i in parents]
            print(f'\nOFFSPRING LIST:')
            pprint.pprint(offspring)
            send_results_to_file({'OFFSPRING LIST':offspring},'a')

    return offspring
    

def mutation(pre_mutation_offspring):

    send_results_to_file({'Mutation Process':'BIT FLIP'},'a')
    # Input: receive the offspring
    print(f'\nREADY FOR MUTATION:')
    pprint.pprint(pre_mutation_offspring)
    send_results_to_file({'READY FOR MUTATION':pre_mutation_offspring},'a')

    # generate random number between 0 and 1 len(chromosome) times.
    post_mutation=[]
    for k in pre_mutation_offspring:
        for i in range(0,NUM_GENES):
            mut_prob=random.random()
            if mut_prob<P_MUTATION:
                print(f'Flipped index: {i}')
                send_results_to_file({'Flipped Index':i},'a')
                if k[1][i]==1:
                    k[1][i]=0
                elif k[1][i]==0:
                    k[1][i]=1
            
        print (f'k:\n{k}')
    
        send_results_to_file({'chromosome after mutation process':k},'a')
        a=k[1].copy()
        post_mutation.append(a)

        send_results_to_file({'wtf':post_mutation},'a')

    return post_mutation


def send_results_to_file(data,file_action):

    if POP_SIZE*GEN_COUNT>OUTPUT_FILE_LIMIT:
        return
    else:
        output_s = pprint.pformat(data)
        with open('output.txt', file_action) as file:
            file.write(output_s)
            file.write('\n\n')
        
def initial_population():
    p=Population()
    send_results_to_file({'Initial Population':p.the_population},'w')
    fitness=[fitness_score(i) for i in p.the_population]
    population_sum=populationSum(fitness)
    w=roulette_weights(fitness)
    n=[f'p{i}' for i in range(len(p.the_population))]
    gen_stat=sorted(list(zip(fitness,p.the_population,w,n)),reverse=True)

    print('population(gen_stat)')
    pprint.pprint(gen_stat)
    print(f'\n')
    send_results_to_file({'Initial Population':gen_stat},'a')

    hall_0f_fame.append(population_sum)

    return gen_stat

def current_population(this_gen):

    fitness=[fitness_score(i) for i in this_gen]
    population_sum=populationSum(fitness)
    w=roulette_weights(fitness)
    n=[f'p{i}' for i in range(POP_SIZE)]
    gen_stat=sorted(list(zip(fitness,this_gen,w,n)),reverse=True)

    print('population(gen_stat)')
    pprint.pprint(gen_stat)
    print(f'\n')
    send_results_to_file({'Generation':gen_stat},'a')

    hall_0f_fame.append(population_sum)

    return gen_stat

def combine_pop_off(population,offspring):

    # extracting the list if chromosomes from the population matrix
    pop=[i[1] for i in population]
    #    
    send_results_to_file({'population':pop},'a')
    send_results_to_file({'offspring of population':offspring},'a')

    # combine the population with its offspring
    combined_solutions=pop+offspring
    send_results_to_file({'Combined Solutions--population and offspring': combined_solutions},'a')

    # get the scores for population and offspring
    scores=[fitness_score(i) for i in combined_solutions]
    send_results_to_file({'scores':scores},'a')
    
    if (OPTIMIZATION=='max'):
        sort_direction=True
    elif(OPTIMIZATION=='min'):
        sort_direction=False

    sorted_combined_solutions=sorted(list(zip(scores,combined_solutions)),reverse=sort_direction)

    send_results_to_file({'sorted combined solutions':sorted_combined_solutions},'a')

    best_solutions=[k[1] for k in sorted_combined_solutions[0:(POP_SIZE)]]

    return best_solutions

def plot_hof(hof):
    x=[i for i in range(GEN_COUNT)]
    y=hof

    if (OPTIMIZATION=='max'):
        opt=max(y)
        opt_words='Max'
    elif(OPTIMIZATION=='min'):
        opt=min(y)
        opt_words='Min'

    
    # t = np.arange(XMIN, XMAX, 0.0001)
    # yy = np.cos(2*np.pi*t) * np.exp(-t) * np.sin(2*np.pi*t)*t**5
    
    
    font = {'family': 'serif',
        'color':  'blue',
        'weight': 'normal',
        'size': 10,
        }

    fig, axs = plt.subplots(1,3, figsize=(15, 5), sharex=False)    
    axs[0].plot(x, y)
    axs[0].set_title(f'POPULATION AVERAGE (y)\n{opt_words} value:{round(opt,4)}',fontdict=font)
    axs[0].grid()
    axs[0].set_xlabel('Generations')
    axs[0].set_ylabel('Population Average')

    variable_names=[f'v{i}' for i in range(1,len(scaled_var_list)+1)]
    m=lambda x:sum(x)/len(x)
    yy=[m(x) for x in zip(*values_list)]
    axs[1].bar(variable_names, yy)
    var_total=round(sum(yy),2)
    axs[1].set_title(f'Variable Amounts (TOTAL:{var_total})',fontdict=font)
    axs[1].grid()
    axs[1].set_xlabel('Variables')
    axs[1].set_ylabel('Variable Values')
    # axs[1].annotate(variable_names[0],scaled_var_list[0])

   
    # print(f'Length of Variable Avg:{len(Variable_avg)}')
    x2=[i for i in range(len(Variable_avg))]
    print(len(x2))
    axs[2].plot(x2[::1000],Variable_avg[::1000])
    axs[2].set_title(f'VARIABLE STUDY:{variable_names[INDEX_TO_STUDY]}',fontdict=font)
    axs[2].grid()
    axs[2].set_xlabel('Sampling of Variable')
    axs[2].set_ylabel(f'VARIABLE STUDY:{variable_names[INDEX_TO_STUDY]}')

    
    e=[i for i in range(0,len(scaled_var_list))]
    
    for j in range(len(variable_names)):
     axs[1].text(variable_names[j],yy[j],round(yy[j],2))

    plt.show()


# %%

if __name__ == '__main__':

    hall_0f_fame=[]
    h=0
    while h<GEN_COUNT:
        if h==0:
            gen_stat=initial_population()
            send_results_to_file({'Generation':h},'a')
            mating_pool=tornament_select(gen_stat,POP_SIZE)
            pre_mutation_offspring=single_point_crossover(mating_pool)
            final_offspring=mutation(pre_mutation_offspring)
            print(f'\nnext generation:')
            pprint.pprint(final_offspring)
            print(f'\n')
            send_results_to_file({'Final Offspring':final_offspring},'a')

            next_gen=combine_pop_off(gen_stat,final_offspring)

            
        else:
            send_results_to_file({'Generation':h},'a')
            send_results_to_file({'This is the new population':next_gen},'a')

            current_gen_stat=current_population(next_gen)
            mating_pool=tornament_select(current_gen_stat,POP_SIZE)
            pre_mutation_offspring=single_point_crossover(mating_pool)
            final_offspring=mutation(pre_mutation_offspring)

            print(f'\nfinal_offspring:')
            pprint.pprint(final_offspring)
            print(f'\n')

            send_results_to_file({'Final Offspring':final_offspring},'a')

            next_gen=combine_pop_off(current_gen_stat,final_offspring)

        # send_results_to_file({'Hall Of Fame':hall_0f_fame},'a')


        h=h+1

    send_results_to_file({'Hall of Fame': hall_0f_fame},'a')

    plot_hof(hall_0f_fame)


    


# %%
