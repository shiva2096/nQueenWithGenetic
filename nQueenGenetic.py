import random 
import numpy as np

# Number of individuals in each generation 
POPULATION_SIZE = 100

# Number of Queens
nQUEEN = 8
 
# Valid genes 
GENES = np.arange(nQUEEN)  # [0,1,2,3,4,5,6,7]


class Individual(object): 
    ''' 
    Class representing individual in population 
    '''
    def __init__(self, chromosome): 
        self.chromosome = chromosome  
        self.fitness = self.cal_fitness() 
  
    @classmethod
    def mutated_genes(self): 
        ''' 
        create random genes for mutation 
        '''
        global GENES 
        gene = random.choice(GENES) 
        return gene 
  
    @classmethod
    def create_gnome(self): 
        ''' 
        create chromosome or string of genes 
        '''
        global nQUEEN 
        return [self.mutated_genes() for _ in range(nQUEEN)] 
  
    def crossover_and_mutate(self, par2): 
        ''' 
        Perform Crossover and Mutations to produce new offspring 
        '''
  
        # chromosome for offspring 
        child_chromosome = [] 
        for gp1, gp2 in zip(self.chromosome, par2.chromosome):     
  
            # random probability   
            prob = random.random() 
  
            # if prob is less than 0.45, insert gene 
            # from parent 1  
            if prob < 0.45: 
                child_chromosome.append(gp1) 
  
            # if prob is between 0.45 and 0.90, insert 
            # gene from parent 2 
            elif prob < 0.90: 
                child_chromosome.append(gp2) 
  
            # otherwise insert random gene(mutate),  
            # for maintaining diversity 
            else: 
                child_chromosome.append(self.mutated_genes()) 
  
        # create new Individual(offspring) using  
        # generated chromosome for offspring 
        return Individual(child_chromosome) 
  
    def cal_fitness(self): 
        ''' 
        Calculate fittness score
        '''
        # For row conflict, subtract the unique no. of elements
        # from the total no. of elements in a chromosome
        fitness = 0
        diff = len(self.chromosome) - len(np.unique(self.chromosome))
        fitness+=diff

        # For diagonal conflict
        for i in range(len(self.chromosome)):
            for j in range(len(self.chromosome)):
                if ( i != j):
                    dx = abs(i-j)
                    dy = abs(self.chromosome[i] - self.chromosome[j])
                    if(dx == dy):
                        fitness += 1
        
        return fitness 
  
# Driver code 
def main(): 
    global POPULATION_SIZE 
  
    #current generation 
    generation = 1
  
    found = False
    population = [] 
  
    # create initial population 
    for _ in range(POPULATION_SIZE): 
                gnome = Individual.create_gnome() 
                population.append(Individual(gnome)) 
  
    while not found: 
  
        # sort the population in increasing order of fitness score 
        population = sorted(population, key = lambda x:x.fitness) 
  
        # if the individual having lowest fitness score ie.  
        # 0 then we know that we have reached to the target 
        # and break the loop 
        if population[0].fitness <= 0: 
            found = True
            break
  
        # Otherwise generate new offsprings for new generation 
        new_generation = [] 
  
        # Perform Elitism, that mean 10% of fittest population 
        # goes to the next generation 
        s = int((10*POPULATION_SIZE)/100) 
        new_generation.extend(population[:s]) 
  
        # From 50% of fittest population, Individuals  
        # will mate to produce offspring 
        s = int((90*POPULATION_SIZE)/100) 
        for _ in range(s): 
            parent1 = random.choice(population[:50]) 
            parent2 = random.choice(population[:50]) 
            child = parent1.crossover_and_mutate(parent2) 
            new_generation.append(child) 
  
        population = new_generation 
  
        # print("Generation: ",generation," | Fittest Chromosome: ",population[0].chromosome, " | Fitness: ",population[0].fitness) 
  
        generation += 1
  
    #print("Generation: ",generation," | Fittest Chromosome: ",population[0].chromosome, " | Fitness: ",population[0].fitness)
    return population[0].chromosome
  
if __name__ == '__main__': 
    fittest_chromosome = main()
    print("Arrangement of Queens: ",fittest_chromosome)
