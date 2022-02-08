import random
import pandas as pd
import copy
import time

def gate(operator, op1, op2):
    if operator == 0:
        return op1 and op2
    elif operator == 1:
        return op1 or op2
    elif operator == 2:
        return not (op1 and op2)
    elif operator == 3:
        return not (op1 or op2)
    elif operator == 4:
        return (op1 and (not op2)) or ((not op1) and op2)
    elif operator == 5:
        return not ((op1 and (not op2)) or ((not op1) and op2))
    else:
        return False
def print_answer(answer):
    print("Answer: ", end=' ')
    for i in range(len(answer)):
        if answer[i] == 0:
            print("AND", end=' ')
        elif answer[i] == 1:
            print("OR", end=' ')
        elif answer[i] == 2:
            print("NAND", end=' ')
        elif answer[i] == 3:
            print("NOR", end=' ')
        elif answer[i] == 4:
            print("XOR", end=' ')
        elif answer[i] == 5:
            print("XNOR", end=' ')
        else:
            return False
    
    
class GeneticAlgorithm:
    def __init__(self):
        self.population = []
        self.population_size = 1000
        self.pool = []
        self.truth_table = pd.read_csv('truth_table.csv')
        self.truth_table.replace('TRUE', True)
        self.truth_table.replace('FALSE', False)
        self.truth_table = self.truth_table.values.tolist()
        self.num_of_rows = len(self.truth_table)
        self.num_of_inputs = len(self.truth_table[0]) - 1
        self.gate_number = self.num_of_inputs - 1

    def fitness(self, chromosome):
        chromosome_fitness = 0

        for i in range(self.num_of_rows):
            output = gate(chromosome[0], self.truth_table[i][0], self.truth_table[i][1])
            for j in range(1, len(chromosome)):
                output = gate(chromosome[j], output, self.truth_table[i][j + 1])
            
            if output == self.truth_table[i][self.num_of_inputs]:
                chromosome_fitness += 1

        return chromosome_fitness
        
    def generate_initial_population(self):
        for i in range(self.population_size):
            new_chromosome = random.choices(range(6), k=self.gate_number)
            new_fitness = self.fitness(new_chromosome)
            self.population.append((new_chromosome, new_fitness))
    
    def selection(self):
        self.pool = []
        self.population.sort(key=lambda x:x[1])

        for i in range(self.population_size):
            self.pool.append(copy.deepcopy(random.choices(self.population, weights=list(range(1,self.population_size + 1)), k=1)[0]))
            
        self.population = []
    
    def crossover(self):
        while self.pool:
            parent1 = self.pool.pop()
            parent2 = self.pool.pop()
            if random.randint(0, self.num_of_rows) > sum(map(lambda x: x[1], self.population)) / self.population_size:
                self.population.append(parent1)
                self.population.append(parent2)
            else:
                index = random.randint(1, self.num_of_inputs - 3)
                child1 = parent1[0][:index] + parent2[0][index:]
                child2 = parent2[0][:index] + parent1[0][index:]
                self.population.append((child1, self.fitness(child1)))
                self.population.append((child2, self.fitness(child2)))
    
    def mutation(self):
        for i in range(self.population_size):
            if random.random() < 1 / self.population_size:
                self.population[i][0][random.randint(0,self.num_of_inputs - 2)] = random.randint(0,5)
    
    def success(self):
        for i in range(self.population_size):
            if self.population[i][1] == self.num_of_rows:
                print("Success!")
                print_answer(self.population[i][0])
                print("\nfitness: ", self.fitness(self.population[i][0]))
                return True
        return False
    
    def evolution_cycle(self):
        self.selection()
        self.crossover()
        self.mutation()
        
    def algorithm(self):
        self.generate_initial_population()

        counter = 0
        while True:
            self.evolution_cycle()
            
            counter += 1
            print("Evolution number: ", counter)
            print("Fitness average: ", sum(map(lambda x: x[1], self.population)) / self.population_size)
            print('<---------------------------->')
            if self.success():
                break
        

GA = GeneticAlgorithm()
time1 = time.time()
GA.algorithm()
time2 = time.time()
print("Time: ", time2 - time1, " s")
print("Finish")
