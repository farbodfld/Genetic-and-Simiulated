#!/usr/bin/python3
import numpy as np
from random import randint, choice, random
import sys
from copy import deepcopy


def init_state(n_varaibles):
    l = []
    for x in range(1, n_varaibles + 1):
        value = randint(0, 1)
        l.append(value)
    return l


def count_incorrect_caluses(input, state):
    clauses = deepcopy(input)
    counter = len(clauses)
    for l in range(len(state)):
        i = 0
        while i < len(clauses):
            if (l in clauses[i] and state[l]) or (-l in clauses[i] and not state[l]):
                clauses.remove(clauses[i])
            else:
                i = i + 1
    return len(clauses)


def genetic(clauses):
    n_varaibles = 100
    iteration = 100
    rate = 0.2
    k = 100
    population = [0] * k
    for i in range(k):
        population[i] = init_state(n_varaibles)

    count = 0
    best = 0
    best_score = 0

    for xx in range(iteration):

        # Sort population
        score = [0] * k
        for i in range(k):
            score[i] = count_incorrect_caluses(clauses[:], population[i])
        for i in range(k):
            for j in range(i, k):
                if score[i] > score[j]:
                    score[i], score[j] = score[j], score[i]
                    population[i], population[j] = population[j], population[i]
        f = 0.0
        for i in population:
            f = f + (len(clauses) - count_incorrect_caluses(clauses[:], population[0])) / float(len(clauses))
        fitness = f / len(population)
        best_score = (len(clauses) - count_incorrect_caluses(clauses[:], population[0])) / float(len(clauses))
        if best_score == 1:
            print("We have a winner!")
            print(population[0])
            return population[0]

        print("Fitness: " + str(fitness) + "****************** Best Score: " + str(best_score))

        cloned_population = []
        chances = []
        for i in range(k):
            chances = chances + ([i] * int((len(clauses) - count_incorrect_caluses(clauses[:], population[i])) / 10))
        for i in range(k):
            cloned_population.append(population[choice(chances)])
        new_population = [0] * k
        for i in range(k):
            limit = randint(0, n_varaibles - 1)
            new_population[i] = cloned_population[randint(0, k - 1)][:limit] + cloned_population[randint(0, k - 1)][
                                                                               limit:]

        krate = random() % rate
        limit = int(len(new_population) * krate)
        for i in range(limit):
            r = randint(0, n_varaibles - 1)
            new_population[randint(2, k - 1)][r] = new_population[i][r] * -1

        new_score = [0] * k
        for i in range(k):
            new_score[i] = count_incorrect_caluses(clauses[:], new_population[i])
        for i in range(k):
            for j in range(i, k):
                if new_score[i] > new_score[j]:
                    new_score[i], new_score[j] = new_score[j], new_score[i]
                    new_population[i], new_population[j] = new_population[j], new_population[i]
        population = population[:int(k * 0.15) + 1] + new_population[:int(k * 0.85)]

    print(str(best_score))


def simulated(clauses):
    scores = []
    n_varaibles = 100
    n_iterations = 1000
    solution = init_state(n_varaibles)
    best_eval = len(clauses) - count_incorrect_caluses(clauses, solution)
    temperature = 5
    for i in range(n_iterations):
        curr = [1 - var if random() < 0.01 else var for var in solution]
        curr_eval = len(clauses) - count_incorrect_caluses(clauses, curr)
        delta = best_eval - curr_eval
        if delta <= 0 or random() < np.exp(-delta / temperature):
            solution = curr
            best_eval = curr_eval
        scores.append(best_eval)
        temperature = (1 - (i + 1) / n_iterations)
        print("iteration " + str(i + 1) + "/" + str(n_iterations) + " Score =" + str(curr_eval / len(clauses)))


if __name__ == "__main__":
    lines = np.loadtxt("database.cnf", dtype=int, delimiter="  ", unpack=False)
    clauses = [line[:-1].tolist() for line in lines]
    print(init_state(100))
    print("[1]: genetic")
    print("[2]: simulated")
    ch = input("Enter your choice: ")
    if ch == "1":
        genetic(clauses)

    elif ch == "2":
        simulated(clauses)
    else:
        print("please enter 1 or 2")