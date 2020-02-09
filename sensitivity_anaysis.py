"""
Sensitivity analysis for the themepark model
Parameters: duration of attractions
OFAT instead of SOBOL, because we have only one parameter so we don't
take into account interaction effects
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle

left_bound = 10
right_bound = 40
problem = {
    'num_vars': 1,
    'names': ['attraction_duration'],
    'bounds': [[left_bound, right_bound]]
}


def notebook():
    # Set the repetitions, the amount of steps, and the amount of distinct values per variable
    replicates = 10 # total number of times to run the model for each combination of parameters
    # max_steps = 100 # Upper limit of steps above which each run will be halted if it hasn't halted on its own.
    distinct_samples = 10 # 20 distinct values for parameter within bounds

    # Set the outputs
    model_reporters = {"Lenghts": []}
    data = {}

    # Get the bounds for this variable and get <distinct_samples> samples within this space (uniform)
    samples = np.linspace(*problem['bounds'][0], num=distinct_samples, dtype=int)
    d = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data=d)
    return df


def plot_param_var_conf(ax, df, var, param):
    """
    Helper function for plot_all_vars. Plots the individual parameter vs
    variables passed.
    Args:
        ax: the axis to plot to
        df: dataframe that holds the data to be plotted
        var: variables to be taken from the dataframe
        param: which output variable to plot
    """
    x = df.groupby(var).mean().reset_index()[var]
    y = df.groupby(var).mean()[param]

    replicates = df.groupby(var)[param].count()
    err = (1.96 * df.groupby(var)[param].std()) / np.sqrt(replicates)

    ax.plot(x, y, c='k')
    ax.fill_between(x, y - err, y + err)

    ax.set_xlabel(var)
    ax.set_ylabel(param)


def plot_all_vars(df, param):
    """
    Plots the parameters passed vs each of the output variables.
    Args:
        df: dataframe that holds all data
        param: the parameter to be plotted
    """

    f, axs = plt.subplots(1)
    plot_param_var_conf(axs, data, 'attdur', param)


if __name__ == "__main__":
    dat = {'attdur': [], 'run': [], 'waiting_time': []}
    tst = pickle.load(open("results/Lotte_5_histo.p", 'rb'))
    mensen = len(tst[0])

    for i in range(3):
        for j in range(25):
            dat['attdur'].append(j)

    for k in range(75):
        dat['run'].append(k)
    for t in tst:
        total = 0
        print('ja1')
        for p in t:
            total += t[p]['totalwaited']
        dat['waiting_time'].append(total/mensen)

    tst2 = pickle.load(open("results/Lotte_10_histo.p", 'rb'))
    for t in tst2:
        total = 0
        print('ja2')
        for p in t:
            total += t[p]['totalwaited']
        dat['waiting_time'].append(total/mensen)

    tst3 = pickle.load(open("results/Lotte_15_histo.p", 'rb'))
    for t in tst3:
        total = 0
        print('ja3')
        for p in t:
            total += t[p]['totalwaited']
        dat['waiting_time'].append(total/mensen)

    data = pd.DataFrame(data=dat)
    plot_all_vars(data, 'waiting_time')
    plt.show()
