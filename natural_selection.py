import random

import numpy as np
import matplotlib.pyplot as plt
from numpy import floor

from DNA import DNA
from bloop import Bloop


class GeneticAlgorithm2:
    def __init__(self, low=1, high=3, ps=0.2, pc=1.0, pm=0.1, max_iter=1000, eps=1e-5, random_state=None):
        self.low = low
        self.high = high
        self.ps = ps  # sample size for selection
        self.pc = pc  # probability for crossover (1 means a crossover must occur)
        self.pm = pm
        self.max_iter = max_iter
        self.eps = eps  # error tolerance
        self.random_state = random_state
        self.best = list()

    def fitness_func(self, bloops):
        """
        Some individuals will compete and those with good fitness will reproduce.
        What we mean by having good fitness is having the objective function optimized.
        f(x) = x, where x is how much food the bloop ate
        We create the equivalent maximization problem as max(f(x)).
        :param x:
        :return:
        """
        return np.array([bloop.nr_food_eaten for bloop in bloops])

    # def decode(self, population):
    #     """
    #     Decode the population. Suppose bin_x represent Decoding function is:
    #     a + reverse_bin(s) * (b-a)/(2^n-1), where:
    #         s belongs to S (the encoded result of X)
    #         a is the lower limit
    #         b is the higher limit
    #         n is the length of s
    #     :param population: an array of binary strings
    #     :return: a decoded array
    #     """
    #     # n = population.shape[1]  # str_size
    #     # x = []
    #     # for s in population:
    #     #     bin_to_int = np.array([int(j) << i for i, j in enumerate(s[::-1])]).sum()
    #     #     int_to_x = self.low + bin_to_int * (self.high - self.low) / (2 ** n - 1)  # decode function
    #     #     x.append(int_to_x)
    #     # return np.array(x)
    #
    #     x = [[bloop.nr_food_eaten for bloop in bloops]]
    #     for s in population:
    #         x.append(int_to_x)

    def selection(self, pop, fitness):
        """
        Tournament Selection.

        Selection is done by taking a sample from the population in the t-th generation for t = 1, 2, …, then from that
        sample, one individual with the best fitness is selected to continue to enter the population in the (t+1)-st
        generation. Individuals in the t-th generation who are not selected will die off.

        This process is carried out m times so that the number of individuals in the population in each generation is
        the same.

        :param pop: the population which is an array of binary strings
        :param fitness: # an array with the fitness result of every individual
        :return:
        """
        # m, n = pop.shape
        m = len(pop)
        new_pop = pop.copy()
        sample_size = self.ps * m

        for index in range(m):
            # get random ids of individuals from population
            rand_id = np.random.choice(m, size=max(1, int(sample_size)), replace=False)
            # get the id of the individual with the maximum fitness result
            max_id = rand_id[fitness[rand_id].argmax()]
            # replace the old individual with the better one in the new population
            new_pop[index] = pop[max_id]

        return new_pop

    def crossover(self, pop):
        """
        Blend Crossover Operator  Crossover. (the variant with α = 0).
        Assuming p1 < p2, this crossover operator creates a random solution in the range [p1, p2].
            p1    first parent
            p2    second parent
            u     random number in [0, 1]

            offspring = (1 - u) * p1 + u * p2
        The blend crossover operator has the interesting property that if the difference between parents is small,
        the difference between the child and parent solutions is also small. So the spread of current population
        dictates the spread of solutions in the resulting population (this is a form of adaptation).
        :param pop: the population
        :return:
        """
        pop_size = len(pop)
        new_pop = pop.copy()

        for i in range(0, pop_size - 1, 2):
            if np.random.uniform(0, 1) < self.pc:
                # choose random u
                u = np.random.uniform(0, 1)
                # blend formula
                new_pop[i].dna.gene = (1 - u) * pop[i].dna.gene + u * pop[i + 1].dna.gene
                new_pop[i + 1].dna.gene = (1 - u) * pop[i+1].dna.gene + u * pop[i].dna.gene

        return new_pop

    def mutation(self, pop):
        """
        Mutation is adding or subtracting 0.02
        :param pop:
        :param pm:
        :return:
        """
        new_pop = []
        width = pop[0].window[0]
        height = pop[0].window[1]
        win = pop[0].win
        canvas = pop[0].canvas

        for bloop in pop:
            new_bloop = Bloop(width, height, DNA(bloop.dna.gene + random.uniform(-0.2, 0.2)), width, height, win, canvas)
            new_pop.append(new_bloop)

        return new_pop

    def plot_result(self, ys, xs, best, iteration_nr, pop_size):
        xval = np.arange(20, 80, 1)
        yval = np.arange(0, 15, 0.25)
        plt.figure(figsize=(10, 5))

        plt.subplot(121)
        plt.plot(xval, yval, color='m')
        plt.scatter(xs, ys, alpha=0.50)
        plt.xlim((20, 80))
        plt.xlabel('size')
        plt.ylabel('food eaten')
        plt.title('Population at Iteration ' + str(iteration_nr) + '\n' +
                  'Number of Individuals: ' + str(pop_size))

        # plt.subplot(122)
        # plt.plot(best, color='c')
        # plt.xlim(0)
        # plt.xlabel('Iteration')
        # plt.ylabel('Best Fitness')
        # plt.title('Best Fitness vs Iteration')

        plt.tight_layout()
        plt.show()

    def start_reproduction_iteration(self, pop):
        np.random.seed(self.random_state)

        # The bloops that ate only once will survive to the next generation but will not reproduce
        filtered_bloops = list(filter(lambda bloop_elem: bloop_elem.nr_food_eaten == 1, pop))
        for bloop in filtered_bloops:  # reset
            bloop.nr_food_eaten = 0
        # The bloops that ate at least twice will survive to the next generation AND will not reproduce
        reproducing_bloops = list(filter(lambda bloop_elem: bloop_elem.nr_food_eaten >= 2, pop))
        x = []
        for bloop in reproducing_bloops:
            x.append(bloop.size)

        if len(filtered_bloops) == 0 and len(reproducing_bloops) == 0:
            print("Population is dead :(")
            return
        if len(filtered_bloops) != 0 and len(reproducing_bloops) == 0:
            print("Population is not dead but there are not children")
            # to do - return this pop
            return
        #
        # for bloop in reproducing_bloops:
        #     print(str(bloop))
        fitness = self.fitness_func(reproducing_bloops)  # an array with the fitness result of every individual
        self.best.append(max(fitness))

        new_pop = self.selection(reproducing_bloops, fitness)
        new_pop = self.crossover(new_pop)
        new_pop = self.mutation(new_pop)

        for old_bloop in filtered_bloops:
            new_pop.append(old_bloop)

        xs = []
        for bloop in reproducing_bloops:
            xs.append(bloop.size)

        self.plot_result(fitness, xs, self.best[-1], 1, len(reproducing_bloops))

        return new_pop
        # print_result(1, pop, fitness, reproducing_bloops)
        #
        # i = 0
        # while i < self.max_iter and abs(best[-1]) > self.eps:
        #     pop = self.selection(pop, fitness)
        #     pop = self.crossover(pop)
        #     pop = self.mutation(pop)
        #     x = self.decode(pop)
        #     fitness = fitness_function(x)
        #     best.append(fitness.max())
        #     i += 1
        #
        # print_result(i, pop, fitness, x)
        #
        # if i == self.max_iter:
        #     print(i, 'maximum iteration reached!')
        #     print('Solution not found. Try increasing max_iter for better result.')
        # else:
        #     print('Solution found at iteration', i)
        #
        # return fitness, x, best, i, self.population_size



def print_result(gen_num, pop, fitness, x):
    """
    Display the population, fitness, and average fitness for the first and last generations. It also displays the best
    fitness as well as point x where the best fitness is achieved.
    :param gen_num: the number of the generation
    :param pop: the population
    :param fitness: the fitness array
    :param x:
    :return:
    """
    m = pop.shape[0]
    print('=' * 68)
    print(f'Generation {gen_num} max fitness {fitness.max():0.4f} at x = {x[fitness.argmax()]:0.4f}')

    for i in range(m):
        print(f'# {i + 1}\t{pop[i]}   fitness: {fitness[i]:0.4f}')

    print(f'Average fitness: {fitness.mean():0.4f}')
    print('=' * 68, '\n')
