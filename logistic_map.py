import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
import glob
import math
import random

#This function takes in the previous value of the logistic map, and the growth rate,
# and performs one iteration. It returns the next value of the logistic map
def iterate(prev, r):
    return r * prev * (1 - prev)

#This function takes in the number of iterations of the logistic map and iterates it over the interval
# from zero to 4. It performs this for 10,000 values of the growth rate in between 0 and 4.
def find_mapping_r(n):
    arr = np.zeros(shape=(10000, n))
    for i in range(10000):
        arr[i,0] = random.random()
    ratios = np.linspace(0, 4, 10000)
    for i in range(1, n):
        arr[:,i] = iterate(arr[:,i-1], ratios)
    print(ratios)
    print(arr)
    #arr_100 = arr[:,50]
    #print(arr_100)
    return ratios, arr

#This function takes in a number and the number of digits we want the number to occupy. It produces
#a representation of the number as a string with digits number of characters, i. e. left_pad(1,3) -> '001',
#left_pad(101, 3) -> '101'
def left_pad(num, digits):
    if num == 0:
        logarithm = 0
    else:
        logarithm = math.log10(num)
    floor = math.floor(logarithm)
    necessary = digits - floor - 1
    string_num = str(num)
    for i in range(necessary):
        string_num = '0' + string_num
    return string_num

#this function produces a single graph of the logistic map values with the x values of ratios, y values of
#values, starting iteration of start_val, and number of values per step of n_values. It saves the resultant
#graph in the folder logistic_gif.
def single_graph(ratios, values, start_val, n_values):
    for i in range(n_values):
        plt.scatter(ratios, values[:,i], 0.0005, marker='o', color='blue')
    plt.title(f'Logistic Map Iterates {start_val} to {start_val + n_values - 1}')
    plt.xlabel('Growth Factor r')
    plt.ylabel('nth Iterate value x\N{LATIN SUBSCRIPT SMALL LETTER N}')
    plt.ylim((-0.1, 1.1))
    plt.figure('')
    plt.savefig(f'logistic_gif/figure_{left_pad(start_val, 3)}.png', dpi = 1000)
    plt.close()

#This function creates an animated gif for n iterations of the logistic map with interval iterations per frame.
#The gif should be opened in a web browser to see what it looks like animated. 
def create_gif(n, interval):
    ratios, all_values = find_mapping_r(n + 1)
    if not os.path.exists(f'logistic_gif'):
        os.mkdir(f'logistic_gif')
    for i in range(n // interval):
        print(i)
        values_sub = all_values[:,1+interval*i:interval + 1 +interval*i]
        single_graph(ratios, values_sub, 1+interval*i, interval)

    frames = []
    imgs = sorted(glob.glob('logistic_gif/figure_*.png'))
    print(imgs)
    for img in imgs:
        frame = Image.open(img)
        frames.append(frame)

    frames[0].save(f'logistic_gif/logistic_gif_{n}.gif', 
                        format='GIF',
                        append_images=frames[1:],
                        save_all=True,
                        duration=600, loop = 0)
        

#A good number of iterations for the gif is 200, with 10 iterations per frame.     

create_gif(50, 1)
