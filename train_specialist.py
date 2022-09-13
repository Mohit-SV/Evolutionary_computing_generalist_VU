import sys
import pdb
import random
import numpy as np
from deap import tools
from deap import base, creator
import time
import numpy as np
from math import fabs,sqrt
import glob, os
import config as C
import argparse

#evoman imports
sys.path.insert(0, 'evoman')
from environment import Environment
from child_controller import player_controller


#no visualisation
os.environ["SDL_VIDEODRIVER"] = "dummy"

# runs simulation
def simulation(env,x):
    f,p,e,t = env.play(pcont=x)
    return f

# evaluation
def evaluate(x, env):
    return np.array(list(map(lambda y: simulation(env,y), x)))


def create_toolboox(cfg, n_vars):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    toolbox.register("attribute", random.uniform,-1,1)
    toolbox.register("Individual", tools.initRepeat, creator.Individual,
                 toolbox.attribute, n=n_vars)
    toolbox.register("population", tools.initRepeat, list, toolbox.Individual)

    toolbox.register("mate", tools.cxUniform, indpb=0.3)#crossover
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=cfg.mutation_step, indpb=cfg.ind_mutpb)#mutation
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", evaluate)
    return toolbox


def evolution(cfg, toolbox, env):
    print("*-"*20)
    print("expt: ", cfg.experiment_name, ", run: ", cfg.run, 'generation:', 0)
    logger = open(f'{cfg.experiment_name}/runs/results_run{cfg.run}.txt', 'w')#take argument
    heading = 'gen,max,mean,std \n'
    logger.write(heading)

    pop = toolbox.population(n=cfg.npop)
    CXPB, MUTPB, NGEN = cfg.cxpb, cfg.mutpb, cfg.ngens

    # Evaluate the entire population
    fitnesses = list(toolbox.evaluate(np.array(pop), env))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = (fit,)
    
    #stats for gen 0
    fits = np.array([ind.fitness.values[0] for ind in pop])
    best = np.max(fits)
    std  =  np.std(fits)
    mean = np.mean(fits)
    print("  Max ", best)
    print("  Avg ", mean)
    print("  Std " , std)

    line = f'0,{best},{mean},{std}\n'
    logger.write(line)
    best_individual = None
    best_individual_fitness = -10000

    for g in range(1, NGEN):
        print("*-"*10)
        print("expt: ", cfg.experiment_name, ", run: ", cfg.run, ', generation:', g)
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.evaluate(np.array(invalid_ind), env)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = (fit,)

        #offspring(variable) is a combination of parents and children
        # previous population replaced by offspring(variable)
        pop[:] = offspring
        fits = np.array([ind.fitness.values[0] for ind in pop])

        best = np.max(fits)
        best_id = np.argmax(fits)

        if best > best_individual_fitness or best_individual_fitness is None:
            best_individual = pop[best_id]
            best_individual_fitness = best

        std  =  np.std(fits)
        mean = np.mean(fits)
        print('End of Generation:', g)
        print("  Max ", best)
        print("  Avg ", mean)
        print("  Std " , std)

        line = f'{g},{best},{mean},{std}\n'
        logger.write(line)
    
    #save best individual amongst all populations
    np.savetxt(f'{cfg.experiment_name}/best/best_run{cfg.run}.txt', np.array(best_individual))

    return best_individual, best_individual_fitness


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg_name', type=str)
    parser.add_argument('--run', type=int, default=1)
    args = parser.parse_args()
    cfg = getattr(C, args.cfg_name)
    cfg.run = args.run


    #make directories to save outputfiles
    if not os.path.exists(cfg.experiment_name):
        os.makedirs(cfg.experiment_name)
        os.makedirs(cfg.experiment_name+'/'+'runs/')
        os.makedirs(cfg.experiment_name+'/'+'best/')

    # initializes simulation in individual evolution mode, for single static enemy.
    env = Environment(experiment_name=cfg.experiment_name,
                  enemies=cfg.enemy_id,
                  playermode="ai",
                  player_controller=player_controller(cfg.n_hidden_neurons),
                  enemymode="static",
                  level=2,
                  speed="fastest",
                  randomini = 'yes',
                  multiplemode = 'yes')    
    
    n_vars = (env.get_num_sensors()+1)*cfg.n_hidden_neurons + (cfg.n_hidden_neurons+1)*5
    
    # create Deap toolbox
    toolbox = create_toolboox(cfg, n_vars)
    # begin evolution 
    evolution(cfg, toolbox, env)
    

    

