import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import time
import pickle

matplotlib.rcParams['font.family'] = ['Heiti TC']
BLOCK_TIME = 3600 * 4

def gumbel_trick(params):
    eps = -np.log(-np.log(np.random.rand(len(params))))
    return params + eps

def enter_items():
    items = list()
    it = input('Enter an item:')
    while it != 'done':
        items.append(it)
        it = input('Enter an item:')
    return [i for i in set(sorted(items))]

def prob_distr(items, scores):
    exp_scores = np.exp(scores) / 0.5
    probs = exp_scores / exp_scores.sum()
    plt.bar(items, probs)
    plt.xlabel('Items')
    plt.ylabel('Probability')
    plt.title('Choose {} !!!'.format(items[np.argmax(probs)]))
    plt.show()

def check_block_time(items):
    with open('block_list.pkl', 'rb') as f:
        bl = pickle.load(f)
    if bl.get(items) == None:
        return
    curr_time = time.time()
    time_diff = curr_time - bl[items]
    if time_diff <= BLOCK_TIME:
        print('Request Denied!!!')
        exit()

if __name__ == '__main__':
    # with open('block_list.pkl', 'wb') as f:
    #     pickle.dump(dict(), f)
    # exit()

    # Read items from command line arguments
    items = list()
    i = 1
    while True:
        try:
            items.append(sys.argv[i])
        except:
            break
        i += 1
    items = sorted([i for i in set(items)])

    check_block_time(tuple(items))

    # Draw sample from the discrete space (Using Gumbel-Max Trick)
    params = np.ones(len(items))
    scores = gumbel_trick(params)
    prob_distr(items, scores)

    # store the current set of items, block for 2 hours
    curr_time = time.time()
    with open('block_list.pkl', 'rb') as f:
        block_list = pickle.load(f)
    block_list[tuple(items)] = time.time()
    with open('block_list.pkl', 'wb') as f:
        pickle.dump(block_list, f)
