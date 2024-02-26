from tasks.tsp import *
from tasks.jssp import *
from evolAlgs import *
from selecSchemes import *
from matplotlib import pyplot as plt

schemes = ["fitnessProportional", "rankBased", "binaryTournament", "truncation", "random"]
parentScheme = schemes[1]; survivalScheme = schemes[3]

def runTSP():
    print("#-------------------------- Travelling Salesman Problem ---------------------------#")
    print("| Number of Generations | Population Size | Mutation Rate | Number of Offsprings |")
    print(f"|         {Num_Generations}           |       {Population_Size}       |      {Mutation_Rate}      |        {Num_Offsprings}           |")
    print(f"\nParent Selection Scheme: {parentScheme}\tSurvival Selection Scheme: {survivalScheme}")

    averageFitnessValues, bestFitnessValues = [], []
    for i in range(Iterations):
        tsp = TSP()
        ea = EvolutionaryAlgorithm(tsp)
        avgFitness_per_Gen, bestFitness_per_Gen = [], []
        for _ in range(Num_Generations):
            print(f"Generation {ea.generation} completed, Best Fitness Value: {abs(ea.getBestFitnessScore())}, Average Fitness Value: {abs(ea.getAvgFitnessScore())}")
            ea.ParentSelection(parentScheme); ea.SurvivalSelection(survivalScheme); ea.localSearchAndReplace()

            bestFitness_per_Gen.append(abs(ea.getBestFitnessScore()))
            avgFitness_per_Gen.append(abs(ea.getAvgFitnessScore()))
        
        averageFitnessValues.append(avgFitness_per_Gen)
        bestFitnessValues.append(bestFitness_per_Gen)
        print(f"\nIteraion {i+1} completed, Best Fitness Value: {bestFitness_per_Gen[-1]}, Average Fitness Value: {avgFitness_per_Gen[-1]}\n")
    
    avg_of_avgFitness = [sum(x) / len(x) for x in zip(*averageFitnessValues)]
    avg_of_bestFitness = [sum(x) / len(x) for x in zip(*bestFitnessValues)]

    plt.plot(avg_of_avgFitness, label="Average Fitness Score")
    plt.plot(avg_of_bestFitness, label="Best Fitness Score")
    plt.annotate(f"{avg_of_avgFitness[-1]:.2f}", 
             (len(avg_of_avgFitness)-1, avg_of_avgFitness[-1]), 
             textcoords="offset points", 
             xytext=(0,10), 
             ha='center', 
             arrowprops=dict(arrowstyle="->", color='blue'))

    plt.annotate(f"{avg_of_bestFitness[-1]:.2f}", 
                (len(avg_of_bestFitness)-1, avg_of_bestFitness[-1]), 
                textcoords="offset points", 
                xytext=(0,-20), 
                ha='center', 
                arrowprops=dict(arrowstyle="->", color='orange'))

    plt.title(r'Fitness Score vs Generation')
    plt.xlabel('Generation'); plt.ylabel('Fitness Score')

    # Add a text box with additional information
    textstr = f'Parent Scheme: {parentScheme}\nSurvival Scheme: {survivalScheme}\nPopulation Size: {Population_Size}\nNumber of Offsprings: {Num_Offsprings}\nMutation Rate: {Mutation_Rate}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.gca().text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

    plt.legend(); plt.show()

def runJSSP():
    print("#-------------------------- Job Shop Scheduling Problem ---------------------------#")
    print("| Number of Generations | Population Size | Mutation Rate | Number of Offsprings |")
    print(f"|         {Num_Generations}           |        {Population_Size}       |      {Mutation_Rate}     |         {Num_Offsprings}           |")
    print(f"\nParent Selection Scheme: {parentScheme}\tSurvival Selection Scheme: {survivalScheme}")
    
    averageFitnessValues, bestFitnessValues = [], []
    file = input("Enter file name: ")
    for i in range(Iterations):
        jssp = JSSP(file)
        ea = EvolutionaryAlgorithm(jssp)
        avgFitness_per_Gen, bestFitness_per_Gen = [], []
        for _ in range(Num_Generations):
            print(f"Generation {ea.generation} completed, Best Fitness Value: {abs(ea.getBestFitnessScore())}, Average Fitness Value: {abs(ea.getAvgFitnessScore())}")
            ea.ParentSelection(parentScheme); ea.SurvivalSelection(survivalScheme)

            bestFitness_per_Gen.append(abs(ea.getBestFitnessScore()))
            avgFitness_per_Gen.append(abs(ea.getAvgFitnessScore()))
        
        averageFitnessValues.append(avgFitness_per_Gen)
        bestFitnessValues.append(bestFitness_per_Gen)
        
        print(f"\nIteraion {i+1} completed, Best Fitness Value: {bestFitness_per_Gen[-1]}, Average Fitness Value: {avgFitness_per_Gen[-1]}\n")
    
    avg_of_avgFitness = [sum(x) / len(x) for x in zip(*averageFitnessValues)]
    avg_of_bestFitness = [sum(x) / len(x) for x in zip(*bestFitnessValues)]

    plt.plot(avg_of_avgFitness, label="Average Fitness Score")
    plt.plot(avg_of_bestFitness, label="Best Fitness Score")
    plt.annotate(f"{avg_of_avgFitness[-1]:.2f}", 
             (len(avg_of_avgFitness)-1, avg_of_avgFitness[-1]), 
             textcoords="offset points", 
             xytext=(0,10), 
             ha='center', 
             arrowprops=dict(arrowstyle="->", color='blue'))
    plt.annotate(f"{avg_of_bestFitness[-1]:.2f}",
                (len(avg_of_bestFitness)-1, avg_of_bestFitness[-1]), 
                textcoords="offset points", 
                xytext=(0,-20), 
                ha='center', 
                arrowprops=dict(arrowstyle="->", color='orange'))
    
    plt.title(r'Fitness Score vs Generation (File: ' + file + ')')
    plt.xlabel('Generation'); plt.ylabel('Fitness Score')
    
    # Add a text box with additional information
    textstr = f'Parent Scheme: {parentScheme}\nSurvival Scheme: {survivalScheme}\nPopulation Size: {Population_Size}\nNumber of Offsprings: {Num_Offsprings}\nMutation Rate: {Mutation_Rate}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.gca().text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=10,
        verticalalignment='top', bbox=props)
    
    plt.legend(); plt.show()

def main():
    prob = input("Please Enter the problem to solve (TSP/JSSP): ")
    if prob == "TSP" or prob == "tsp": runTSP()
    elif prob == "JSSP" or prob == "jssp": runJSSP()
    else: print("Invalid Problem Name! Please enter either TSP / tsp or JSSP / jssp.")

if __name__ == "__main__":
    main()