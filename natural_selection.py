import numpy as np
import matplotlib.pyplot as plt


class GeneticAlgorithm:
    def __init__(self, func, pop_size, str_size, low, high,
                 ps=0.2, pc=1.0, pm=0.1, max_iter=1000, eps=1e-5, random_state=None):
        self.func = func
        self.population_size = pop_size
        self.binary_string_size = str_size
        self.low = low
        self.high = high
        self.ps = ps  # sample size for selection
        self.pc = pc  # probability for crossover (1 means a crossover must occur)
        self.pm = pm
        self.max_iter = max_iter
        self.eps = eps  # error tolerance
        self.random_state = random_state

    def init_population(self):
        """
        Initialize population
        """
        return np.random.randint(2, size=(self.population_size, self.binary_string_size))

    def decode(self, population):
        """
        Decode the population. Suppose bin_x represent Decoding function is:
        a + reverse_bin(s) * (b-a)/(2^n-1), where:
            s belongs to S (the encoded result of X)
            a is the lower limit
            b is the higher limit
            n is the length of s
        :param population: an array of binary strings
        :return: a decoded array
        """
        n = population.shape[1]  # str_size
        x = []
        for s in population:
            bin_to_int = np.array([int(j) << i for i, j in enumerate(s[::-1])]).sum()
            int_to_x = self.low + bin_to_int * (self.high - self.low) / (2 ** n - 1)  # decode function
            x.append(int_to_x)
        return np.array(x)

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
        m, n = pop.shape
        new_pop = pop.copy()
        sample_size = self.ps * m

        for index in range(m):
            # get random ids of individuals from population
            rand_id = np.random.choice(m, size=max(1, int(sample_size)), replace=False)
            # get the id of the individual with the maximum fitness result
            max_id = rand_id[fitness[rand_id].argmax()]
            # replace the old individual with the better one in the new population
            new_pop[index] = pop[max_id].copy()

        return new_pop

    def crossover(self, pop):
        """
        One-point Crossover. An index for the binary string is randomly chosen, and then the bits after the index
        are swiped with the bits from the other parent.
        :param pop: the population which is an array of binary strings
        :param pc:
        :return:
        """
        pop_size, str_size = pop.shape
        new_pop = pop.copy()

        for i in range(0, pop_size - 1, 2):
            if np.random.uniform(0, 1) < self.pc:
                # choose random index
                pos = np.random.randint(0, str_size - 1)
                # interchange the bits of the two parents which have the position after the index
                new_pop[i, pos + 1:] = pop[i + 1, pos + 1:].copy()
                new_pop[i + 1, pos + 1:] = pop[i, pos + 1:].copy()

        return new_pop

    def mutation(self, pop):
        """
        Mutation is doing an inversion (from 0 to 1 or from 1 to 0) for each bit in each individual in the population of
        the t-th generation.
        :param pop:
        :param pm:
        :return:
        """
        pop_size, str_size = pop.shape
        new_pop = pop.copy()
        # generate array of binary strings. If the number generate is < pm it means it's true => the bit 1.
        mutation_prob = (np.random.uniform(0, 1, size=(pop_size, str_size)) < self.pm).astype(int)
        # sum the two arrays and divide by 2 to make the inversion.
        return (mutation_prob + new_pop) % 2

    def start_algo(self):
        np.random.seed(self.random_state)
        pop = self.init_population()
        x = self.decode(pop)
        fitness = fitness_function(x)  # an array with the fitness result of every individual
        best = [fitness.max()]
        print_result(1, pop, fitness, x)

        i = 0
        while i < self.max_iter and abs(best[-1]) > self.eps:
            pop = self.selection(pop, fitness)
            pop = self.crossover(pop)
            pop = self.mutation(pop)
            x = self.decode(pop)
            fitness = fitness_function(x)
            best.append(fitness.max())
            i += 1

        print_result(i, pop, fitness, x)

        if i == self.max_iter:
            print(i, 'maximum iteration reached!')
            print('Solution not found. Try increasing max_iter for better result.')
        else:
            print('Solution found at iteration', i)

        return fitness, x, best, i, self.population_size


def fitness_function(x):
    """
    Some individuals will compete and those with good fitness will reproduce.
    What we mean by having good fitness is having the objective function optimized.
    f(x) = sin(x) - x/2
    We create the equivalent maximization problem as max(-|f(x)|).
    :param x:
    :return:
    """
    return -np.abs(np.sin(x) - 0.5 * x)


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


def plot_result(func, fs, xs, best, i, m):
    xval = np.arange(1, 3, 0.01)
    yval = func(xval)
    plt.figure(figsize=(10, 5))

    plt.subplot(121)
    plt.plot(xval, yval, color='m')
    plt.scatter(xs, fs, alpha=0.50)
    plt.xlim((1, 3))
    plt.xlabel('$x$')
    plt.ylabel('$f(x) = -|sin(x) - 0.5x|$')
    plt.title('Population at Iteration ' + str(i) + '\n' + \
              'Number of Individuals: ' + str(m))

    plt.subplot(122)
    plt.plot(best, color='c')
    plt.xlim(0)
    plt.xlabel('Iteration')
    plt.ylabel('Best Fitness')
    plt.title('Best Fitness vs Iteration' + '\n' + \
              'Number of Individuals: ' + str(m))

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    ga = GeneticAlgorithm(fitness_function, pop_size=15, str_size=20, low=1, high=3, random_state=69)
    fs, xs, best, i, m = ga.start_algo()
    plot_result(fitness_function, fs, xs, best, i, m)
