from tasks.problem import Problem
from selecSchemes import SelectionSchemes

# Parameters
Population_Size = 100
Num_Offsprings = 70
Num_Generations = 100
Mutation_Rate = 0.95
Iterations = 1

class EvolutionaryAlgorithm:
    """
    This class will be responsible for the evolutionary cycle, including the parent selection, and survival selection implementations.
    """

    def __init__(self, problem: Problem) -> None:
        """
        The constructor method for the EvolutionaryAlgorithm class. It initializes the attributes of the class including the problem, population, fitness values, and the generation number.
        Args:
            - problem (Problem): The problem object to be solved (TSP or JSSP).
        
        Returns:
            - None
        """
        self.problem = problem
        self.population = self.problem.population
        self.fitnessVals = self.problem.fitnessVals
        self.generation = 1
    
    def getBestFitnessScore(self):
        """ Returns the best Fitness Score """
        return max(self.fitnessVals)

    def getBestIndiv(self):
        """ Returns the best individual """
        return self.population[self.fitnessVals.index(self.getBestFitnessScore())]

    def getWorstFitnessScore(self):
        """ Returns the worst Fitness Score """
        return min(self.fitnessVals)        

    def getWorstIndiv(self):
        """ Returns the worst individual """
        return self.population[self.fitnessVals.index(self.getWorstFitnessScore())]

    def getAvgFitnessScore(self):
        """ Returns the average Fitness Score """
        return sum(self.fitnessVals)/len(self.fitnessVals)

    def ParentSelection(self, selection: str) -> None:
        """
        Generates an offspring from the population, based on the selection method used. 
        Args:
            - selection: The selection method to be used as a string

        Returns:
            - None 
        """
        selectionMethod = getattr(SelectionSchemes, selection)
        parents = selectionMethod(self.population, self.fitnessVals, Num_Offsprings)
        for i in range(0, Num_Offsprings, 2):
            bacha1, bacha2 = self.problem.crossover(parents[i], parents[i+1]), self.problem.crossover(parents[i], parents[i+1])
            self.population.append(self.problem.mutate(Mutation_Rate, bacha1))
            self.population.append(self.problem.mutate(Mutation_Rate, bacha2))


    def SurvivalSelection(self, selection: str) -> None:
        """
        This method will evaluate the chromosomes in our population based on the selection method used. An elitism approach is used inherently for survival selection. This elitism approach was used after a trial and error, and it was found that the elitism approach was effective overall inherently. 
        Args:
            - selection: The selection method to be used as a string

        Returns:
            - None 
        """
        self.problem.population = self.population
        self.fitnessVals = self.problem.fitness()

        selection_method = getattr(SelectionSchemes, selection)
        newGen = selection_method(self.population, self.fitnessVals, Population_Size - 1)

        bestIndiv = self.getBestIndiv()
        newGen.append(bestIndiv)

        self.population = newGen
        self.problem.population = self.population
        self.fitnessVals = self.problem.fitness()
        self.generation += 1

    def localSearchAndReplace(self):
        """
        This method will perform local search on the best individual and replace the worst individual with the mutated best individual if the mutated best individual has a better fitness score than the either the best individual, or the average fitness of the population. Thus, this can potentially lead us out of sub-optimal solutions.
        """
        bestChromosome = self.getBestIndiv()
        mutatedBest = self.problem.mutate(1.1, bestChromosome)
        mutatedFitness = self.problem.fitnessHeper(mutatedBest)

        if mutatedFitness > self.getBestFitnessScore() or mutatedFitness >= self.getAvgFitnessScore():
            worstIndex = self.fitnessVals.index(self.getWorstFitnessScore())
            self.population[worstIndex] = mutatedBest
            self.fitnessVals[worstIndex] = mutatedFitness
