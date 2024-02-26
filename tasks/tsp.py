from tasks.problem import Problem
from evolAlgs import *
from selecSchemes import *
import random
import numpy as np
from multiprocessing import Pool

class TSP(Problem):
    """
    This class will be the implementation for the Travelling Salesman Problem. It will be responsible to load data, contian chromosome representation, and fitness function.
    """

    def __init__(self) -> None:
        """"
        Initializes the TSP Class, loads data from the file, initializes the population, and stores the fitness of the population.
        """
        self.cities = {}; self.loadData()
        self.population = self.initializePopulation(); self.fitnessVals = self.fitness()

    def loadData(self) -> None:
        """ This method will load the data from the file and store it in the class, converting it into a chromosome representation. """
        with open("data/qa194.tsp") as f:
            for city in f.readlines()[7:-1]:
                city = city.split()
                self.cities[int(city[0])] = (float(city[1]), float(city[2]))
        f.close()

    def initializePopulation(self) -> list:
        """
        This method will initialize the population. The population will be a list of chromosomes, where each chromosome is a list of cities. The initiliazation will be done using the nearest neighbor heuristic, which helps in generating a good initial population as there is a 90% chance that for every random city that is selected, either the nearest city to it, or the nearest two cities are selected. This makes the fitness scores really good to start with as then on average 90% of the population will have a relatively good fitness score.

        Args:
            - None
        
        Returns:
            - A list of chromosomes
        """
        cityData = list(self.cities.keys())
        population = []
        for _ in range(Population_Size):
            if random.random() < 0.9:
                startCity = random.choice(cityData)
                unvisitedCities = cityData[:]
                unvisitedCities.remove(startCity)
                tour = [startCity]
                while unvisitedCities:
                    nearestCity = min(unvisitedCities, key=lambda city: self.distanceHelper(tour[-1], city))
                    unvisitedCities.remove(nearestCity)
                    tour.append(nearestCity)
                    if unvisitedCities:
                        secondNearestCity = min(unvisitedCities, key=lambda city: self.distanceHelper(tour[-1], city))
                        unvisitedCities.remove(secondNearestCity)
                        tour.append(secondNearestCity)
                population.append(tour)
            else:
                random.shuffle(cityData)
                population.append(cityData.copy())
        return population
    
    def distanceHelper(self, city1: int, city2: int) -> float:
        """
        This method will calculate the distance between two cities.
        Args:
            - city1: The first city
            - city2: The second city
        
        Returns:
            - The distance between the two cities as a floating point number
        """
        x1, y1 = self.cities[city1]; x2, y2 = self.cities[city2]
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def fitnessHeper(self, chromosome: list)-> float:
        """
        This method will calculate the fitness of a chromosome. It is to be used as a helper for the overall fitness, but also can be used to calculate the fitness of a single chromosome. (The "heper" is a typo that was realized too late to go back and change throughout the code :) )
        Args:
            - chromosome: The chromosome to be evaluated
        
        Returns:
            - The fitness of the chromosome
        """
        totalDistance = 0
        for i in range(len(chromosome) - 1):
            totalDistance += self.distanceHelper(chromosome[i], chromosome[i+1])
        totalDistance += self.distanceHelper(chromosome[0], chromosome[-1])
        return totalDistance*-1

    def fitness(self) -> list:
        """
        This method will calculate the fitness of our population. Pool is used to parallelize the fitness calculation, to reduce time taken. (Although in the grand scheme of things I don't think this does much help now)
        Args:
            - None
        
        Returns:
            - The fitness of our chromosome population
        """
        with Pool() as p:
            return p.map(self.fitnessHeper, self.population)
    
    def mutate(self, rate: float, chromosome: list) -> list:
        """
        This method will perform mutation on a chromosome based on the rate of mutation which is our probability.
        Args:
            - rate: The probability of mutation
            - chromosome: The chromosome to be mutated
        
        Returns:
            - The mutated chromosome
        """
        if random.random() < rate:
            p1 = random.randint(0, len(chromosome)-1); p2 = random.randint(p1, len(chromosome)-1)
            mid = chromosome[p1:p2]; begin = chromosome[:p1]; end = chromosome[p2:]
            chromosome = begin + mid[::-1] + end
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
        return bacha