from environment import Environment
from time import sleep
from random import randint
import utils


def random_going():
    while True:
        acts = env.get_actions()
        acts[randint(0, len(acts) - 1)]()
        print(env)
        print('loss: ', env.loss())
        sleep(1)


def heuristic_debug():
    memory_stack = []
    while env.loss():
        acts = list(zip(env.get_actions(), env.get_scores()))
        acts.sort(key=lambda x: x[1])
        if len(acts):
            acts[0][0]()
            memory_stack.append(acts[0][0])
            env.remind()
        else:
            env.get_anti_func(memory_stack[-1])()
            del memory_stack[-1]
        print(env)
        print('loss: ', env.loss())
        print(env.loss(True))
        sleep(2)


def heuristic():
    steps = 0
    memory_stack = []
    while env.loss():
        acts = list(zip(env.get_actions(), env.get_scores()))
        acts.sort(key=lambda x: x[1])
        if len(acts):
            acts[0][0]()
            memory_stack.append(acts[0][0])
            env.remind()
        else:
            env.get_anti_func(memory_stack[-1])()
            del memory_stack[-1]
        steps += 1
        if not steps % 1000:
            print(steps)
    return steps


if __name__ == '__main__':

    print('Введите начальное состояние')
    start_state = utils.input_matrix(3, file='start.txt')
    print('Введите конечное состояние')
    finish_state = utils.input_matrix(3, file='finish.txt')

    env = Environment(start_state, finish_state)
    print(heuristic())
