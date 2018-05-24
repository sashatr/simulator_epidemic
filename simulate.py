#!/usr/bin/env python3.5

# >`chmod u+x simulate.py` get access mode for start script on linux
# >remove .py for use `./simulate -n 20 -i 1000 --your-algorithm`
# instead `./simulate.py -n 20 -i 1000 --your-algorithm`

import random
import argparse


class Node:
    global_id = 0

    def __init__(self):
        self.step = False
        self.id = Node.global_id
        Node.global_id += 1

    def infection(self):
        self.step = True

    def disinfection(self):
        self.step = False

    def __str__(self):
        return '{}-{}'.format(self.id, self.step)

    def __repr__(self):
        return '{}-{}'.format(self.id, self.step)


def random_choice(index, nodes, X):
    while True:
        rcs = random.sample(nodes, X)
        if index in rcs:
            continue
        else:
            return rcs


def infection(nodes, index, X):
    new_infected = 0
    new_inf = []

    for node in index:
        rr = random_choice(node, nodes, X)

        for r in rr:
            if r.step is False:
                r.infection()
                new_infected += 1
                new_inf.append(r)
    return nodes, new_inf, new_infected


def start(MY_ALG, nodes, X):
    index = [random.choice(nodes)]
    index[0].infection()

    n_iter = 0
    belay = 0

    while True:
        n_iter += 1
        r = infection(nodes, index, X)
        nodes, index = r[0], r[1]

        if MY_ALG:
            if r[2] is 0:
                belay += 1
                if belay is not 4:  # WHY 4?
                    continue
                else:
                    break
        else:
            if r[2] is 0:
                break

    success = False
    for node in nodes:
        if node.step is False:
            pass
        else:
            success = True

    return nodes, n_iter, success


def run_sim(MY_ALG, N_NODES, X, ITER, ITER_ALG):
    success = 0
    n_iter_ = 0
    nodes = [Node() for _ in range(0, N_NODES)]

    for iter in range(0, ITER):
        t = start(MY_ALG, nodes, X)
        n_iter_ += t[1]
        if t[2] is True:
            success += 1

        nodes = t[0]
        for node in nodes:
            node.disinfection()

    res = round(success/ITER*100, 2)
    n_iter = round(n_iter_/ITER, 0)
    if ITER_ALG:
        return 'In {}% cases all nodes received the packet.\nAverage number: {}'.format(res, n_iter)
    else:
        return 'In {}% cases all nodes received the packet.'.format(res)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--nodes', type=int, help='Number of nodes in the network simulator', required=True)
    parser.add_argument('-i', '--iterations', type=int, help='Number of simulations',  required=True)
    parser.add_argument('--your-algorithm', nargs='?', help='To use the improved algorithm', default='OK')
    parser.add_argument('--iter-algorithm', nargs='?', help='Number of iterations of the algorithm', default='OK')

    args = vars(parser.parse_args())

    N_NODES = args['nodes']
    X = 4
    ITER = args['iterations']

    if args['your_algorithm'] is None:
        MY_ALG = True
    else:
        MY_ALG = False

    if args['iter_algorithm'] is None:
        ITER_ALG = True
    else:
        ITER_ALG = False

    return run_sim(MY_ALG, N_NODES, X, ITER, ITER_ALG)


if __name__ == '__main__':
    print(main())