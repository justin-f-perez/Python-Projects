'''
This script runs a series of tests measuring the deviation of an estimated 
median from the actual median for three different types of randomized numbers 
(random-types). The estimates are created by taking the median of a random subset 
of a list of random numbers. The size of this subset is in range(4, 128, 4). For 
each sample size and random-type combination, 20 trials are conducted and 
averaged. These averages are then graphed on a line plot with one line for each of 
the three random-types. There are three types of randomized numbers: uniform, 
normal, and exponential. The tests are run and the results are displayed 
automatically upon running this script. To run the tests again and display the new 
results, simply execute the run_test() function.

This module depends on matplotlib.

Author: Justin Perez
Release Date: 12/10/2013
'''

import matplotlib.pyplot as plt
import random as rng

def experimental_data(mode, length=16384):
    '''
    Generates a list of random numbers.
    
    Input:
        length is expected to be an integer representing the number of random
            data elements to be returned. 
            Default value: 16384 
        mode is expected to be one of the following strings: 
            "Uniform", "Normal", and "Exponential". 
            -Uniform uses the standard Python random.random() 
            -Normal uses random.gauss() and data binning
            -Exponential uses exponentially distributed random numbers (also 
                data binned.)
                
    Output:
        A list of random numbers of len(length) generated using the methodology
            described by mode.
    '''
    L = None
    if mode.lower()=="uniform":
        L = [rng.random() for i in range(length)]
    elif mode.lower()=="normal":
        L = [rng.gauss(mu=10.0, sigma=3.0) for i in range(length)]
        L = [round(val*10.0)/10.0 for val in L]
    elif mode.lower()=="exponential":
        L = [rng.expovariate(1/10.0) for i in range(length)]
        L = [round(val*10.0)/10.0 for val in L]
        
    #if L is still None then the user entered a bad mode
    if L == None:
        raise Exception("Please choose a valid mode. " + mode + " is not valid.")
    else:
        return L
        
def score_median(data_mode, sample_size):
    '''
    Runs and scores a median approximation. 
    
    Input:
        data_mode is expected to be one of the following strings: 
            "Uniform", "Normal", and "Exponential". 
            -Uniform uses the standard Python random.random() 
            -Normal uses random.gauss() and data binning
            -Exponential uses exponentially distributed random numbers (also 
                data binned.)
        sample_size is how many numbers should be in the randomly selected sample
            (of a list of 16384 random numbers) to construct the estimated median.
            
    Output:
        Returns the score for the estimation. The score is the difference between
            the estimated and actual medians, divided by the actual median. 
    '''
    data = experimental_data(data_mode)
    data.sort()
    actual_median = data[len(data)//2]
    sorted_sample = sorted(rng.sample(data, sample_size))
    estimated_median = sorted_sample[len(sorted_sample)//2]
    score = abs(estimated_median - actual_median)/actual_median
    return score   
    
def median_line_plot(uniform_results, normal_results, exponential_results):
    '''
    Constructs and displays a line plot of the scoring results for the uniform, 
    normal, and exponential random number median estimates. 
    Input:
        Each input is a dictionary whose keys represent the sample size of 
            the list of data on which the estimated median was calculated. The 
            values represent the average score for 20 trials. The score is the 
            difference between the estimated median and the actual median, divided 
            by the actual median. The names of the inputs correspond to the
            methodology used to generate the initial, full (unsampled) list of 
            numbers (e.g., uniform_results corresponds to a data set generated
            by using experimental_data(mode="uniform").)
    
    Output:
        Displays a line plot graph with each line representing median-estimates
        for a different type of randomly generated number (uniform, normal,
        or exponential). The x-axis represents the sample size of numbers used
        to estimate the median. The y-axis represents the averaged score of 20
        trials. Score is the difference between the estimated median and the
        actual median, divided by the actual median.
    '''
    #items need to be sorted by their x-value or else the line will go 'backwards'
    uniform_items = list(zip(*sorted(uniform_results.items())))
    normal_items = list(zip(*sorted(normal_results.items())))
    exponential_items = list(zip(*sorted(exponential_results.items())))
    
    plt.plot(uniform_items[0], uniform_items[1], color="red")
    plt.plot(normal_items[0], normal_items[1], color="blue")
    plt.plot(exponential_items[0], exponential_items[1], color="grey")
    
    plt.title("Uniform (red) vs Normal (blue) vs Exponential (grey) \n" +
        "Median Estimators", color="green")
    plt.xlabel("sample size of median estimate")
    plt.ylabel("score (smaller is better)")
    plt.show()

def run_test():
    '''
        This is the main function for the script. See the docstring for this
        script for more information.
    '''
    sample_sizes = range(4,128,4)
    #can't use a=b=c={} or else they'll alias the same dict.
    uniform_results, normal_results, exponential_results = {}, {}, {}
    #runs 20 tests for each sample size and random-type and stores the average of the 20 runs for each random-type
    for sample_size in sample_sizes:
        uniform_results[sample_size] = sum([score_median("uniform", sample_size) for i in range(20)]) / 20
        normal_results[sample_size] = sum([score_median("normal", sample_size) for i in range(20)]) / 20
        exponential_results[sample_size] = sum([score_median("exponential", sample_size) for i in range(20)]) / 20
    median_line_plot(uniform_results, normal_results, exponential_results)

#The tests should run and the results should display upon this script's execution
run_test()
