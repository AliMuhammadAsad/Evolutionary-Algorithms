from tasks.problem import Problem
from evolAlgs import *
from selecSchemes import *
import random

class JSSP(Problem):
    """
    This class will be the implementation for the Job Shop Scheduling Problem. It will be responsible to load data, contian chromosome representation, and fitness function.
    """

    def __init__(self, filename: str) -> None:
        """
        Initializes the JSSP Class, loads data from the file, initializes the population, and stores the fitness of the population.
        Args:
            - filename (str): The name of the file to be loaded.

        Returns:
            - None
        """
        self.data = {}
        self.loadData(filename)
        self.population = self.initializePopulation()
        self.fitnessVals = self.fitness()

    def loadData(self, filename: str) -> None:
        """
        This method will load the data from the file and store it in the class, converting it into a chromosome representation.
        
        Args:
            - filename (str): The name of the file to be loaded.

        Returns:
            - None
        """
        with open(f"data/{filename}.txt", 'r') as f:
            lines = f.readlines()
            jobMachineData = lines[2:]
            for i, line in enumerate(jobMachineData):
                jobData = line.split()
                self.data[i] = [(int(jobData[j]), int(jobData[j+1])) for j in range(0, len(jobData), 2)]

    def initializePopulation(self) -> list:
        """
        Initializes the population. A single chromosome represents a schedule of operations. Each operation is represented by a tuple (job, machine). Random permutations of the operations are generated to form the initial population. 
        """
        population = []
        for _ in range(Population_Size):
            operations = [(job, machine) for job, jobData in self.data.items() for machine, _ in jobData]
            random.shuffle(operations)
            population.append(operations)
        return population

    def fitnessHeper(self, chromosome: list) -> list:
        """
        This method will calculate the fitness of a chromosome. It is to be used as a helper for the overall fitness, but also can be used to calculate the fitness of a single chromosome. (The "heper" is a typo that was realized too late to go back and change throughout the code :) )
        Fitness is found by keeping track of when a machine and job finishes its current operation. Each operation in the chromosome is iterated over, and the start and end times are calculated. The fitness is the maximum end time of all the machines.
        Args:
            - chromosome: The chromosome to be evaluated
        
        Returns:
            - The fitness of the chromosome
        """
        machineEndTimes = {machine: 0 for machine in range(len(self.data[0]))}
        jobEndTimes = {job: 0 for job in self.data.keys()}

        for job, machine in chromosome:
            _, processTime = next((m, t) for m, t in self.data[job] if m == machine)
            startTime = max(machineEndTimes[machine], jobEndTimes[job])
            endTime = startTime + processTime
            machineEndTimes[machine] = endTime
            jobEndTimes[job] = endTime
        fitness = max(machineEndTimes.values())
        return fitness*-1

    def fitness(self) -> list:
        """ Uses the fitness helper function to calculate the total fitness of the population"""
        return [self.fitnessHeper(chromosome) for chromosome in self.population]

    def mutate(self, rate: float, chromosome: list) -> list:
        """
        This method will mutate the chromosome. The mutation is done by swapping two operations in the chromosome. The mutation rate is used to determine the probability of mutation. Insertion mutation is used for this. 

        Args:
            - rate (float): The mutation rate
            - chromosome (list): The chromosome to be mutated

        Returns:
            - The mutated chromosome
        """
        # Insert Mutation
        if random.random() < rate:
            p1 = random.randint(0, len(chromosome)-1)
            p2 = random.randint(0, len(chromosome)-1)
            while p1 == p2:
                p2 = random.randint(0, len(chromosome)-1)
            operation = chromosome.pop(p1)
            chromosome.insert(p2, operation)
        return chromosome

    def crossover(self, parent1: list, parent2: list) -> list:
        """
        This method will perform crossover between two parents and return a child.
        Args:
            - parent1: The first parent
            - parent2: The second parent
        
        Returns:
            - A child chromosome (list)
        """
        point1 = random.randint(0, len(parent1)-1); point2 = random.randint(point1, len(parent1)-1)
        middle = parent1[point1:point2]; first = parent2[0:point1]; end = parent2[point2:len(parent2)]
        
        for i in range(len(end)):
            if end[i] in middle: end[i] = parent1[point2 + i]
        
        for i in range(len(first) -1, -1, -1):
            if first[i] in middle and first[i] not in end: first[i] = parent1[i - point1]
        
        bacha = first + middle + end
        
        for i in range(len(bacha)):
            if bacha.count(bacha[i]) > 1:
                if parent1[i] not in bacha: bacha[i] = parent1[i]
                elif parent2[i] not in bacha: bacha[i] = parent2[i]
                else: bacha[i] = [x for x in parent1 if x not in bacha][0]
        for each in bacha: assert bacha.count(each) == 1, f"Each city should be visited only once"
        return bacha
