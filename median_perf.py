'''
This script runs a performance test measuring the amount of time it takes for
two median algorithms to execute for lists of random data. These lists of random
data are of lengths range(2**10,2**19,2**15). For each length, the script
will generate a list of random data and use each median algorithm on it 5 times,
storing the average of those 5 results. The average for each length is then used
to construct a line plot for each algorithm's results. The tests are run and
the results are displayed automatically upon running this script. To run the
tests again and display the new results, simply execute the run_test() function.

This module depends on matplotlib.

Author: Justin Perez
Release Date: 12/10/2013
'''

import random as rng
import heapq as hq
import time
import matplotlib.pyplot as plt

def experimental_data(length):
    '''
    Generates a list of random numbers.
    
    Input:
        length is how many random numbers should be in the returned list
    Output:
        A list of random numbers as long as was specified by the length parameter.
        Uses the standard Python random.random() for number generation.
    '''
    return [rng.random() for i in range(length)]

def heap_median(L):
    '''
    Calculates the median value for a list of numbers using a heap queue algorithm.
    
    Input:
        L is a list of numbers on which to calculate the median.
    Output:
        The median value of the list.
    '''
    hq.heapify(L)
    for n in range(len(L)//2):
        hq.heappop(L)
    return hq.heappop(L)

def sort_median(L):
    '''
    Calculates the median value for a list of numbers using a sorting algorithm.
    
    Input:
        L is a list of numbers on which to calculate the median.
    Output:
        The median value of the list.
    '''
    sL = sorted(L)
    return sL[len(L)//2]

def median_line_plot(sorted_results, heap_results):
    '''
    Constructs a line plot of the performance results for the sorting and
    heap queue median algorithms.
    Input:
        sorted_results is a dictionary whose keys represent the length of the list
            of data on which the median was calculated using a sorting algorithm
            and whose values represent the amount of time the algorithm took to
            execute.
        heap_results is a dictionary whose keys represent the length of the list
            of data on which the median was calculated using a heap queue 
            algorithm and whose values represent the amount of time the 
            algorithm took to execute.
    
    Output:
        Displays a line plot graph with a cyan line representing the sort median
            performance results and a magenta line representing the heap queue
            median results. The length of the list of random data for which the
            median value was calculated is displayed on the x-axis, while
            the time the algorithm took to execute is on the y-axis.
    '''
    #items need to be sorted by their x-value or else the line will go 'backwards'
    sorted_items = list(zip(*sorted(sorted_results.items())))
    heap_items = list(zip(*sorted(heap_results.items())))
    
    plt.plot(sorted_items[0], sorted_items[1], color="cyan")
    plt.plot(heap_items[0], heap_items[1], color="magenta")
    
    plt.title("Sort Median (cyan) vs Heap Median (magenta)", color="green")
    plt.xlabel("length of list")
    plt.ylabel("computing time (seconds)")
    plt.show()

def time_median(median_func, length):
    '''
    Runs and times a performance test.
    
    Input:
        median_func is the function to be tested. This function should accept
            a list of numbers and return the median value.
        length is how long the list of random numbers that will be used to test
            the median function should be.
            
    Output:
        Returns the amount of CPU time, in seconds, that it took to calculate
            the median.
    '''
    data = experimental_data(length)
    start_time = time.clock()
    median_func(data)
    end_time = time.clock()
    total_time = end_time - start_time
    return total_time

def run_test():
    '''
        This is the main function for the script. See the docstring for this
        script for more information.
    '''
    lengths = range(2**10, 2**19, 2**15)
    #can't use sorted_results=heap_results={} or else they'll alias the same dict.
    sorted_results, heap_results = {}, {}
    #runs 5 tests for each length and each algorithm (for a total of 10) and stores the average of the 5 runs for each algorithm
    for length in lengths:
        sorted_results[length] = sum([time_median(sort_median, length) for i in range(5)])/5
        heap_results[length] = sum([time_median(heap_median, length) for i in range(5)])/5
    median_line_plot(sorted_results, heap_results)

#The tests should run and the results should display upon this script's execution
run_test()
