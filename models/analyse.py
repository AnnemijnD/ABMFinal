import pickle
import matplotlib.pylab as plt
from matplotlib.lines import Line2D
import numpy as np
import seaborn as sns
sns.set()

RUNS = 100
STRATEGIES = ["Random", "0.00", "0.25", "0.50", "0.75", "1.00"]


def plot_boxplots():
    """
    Plot total amount of rides and waiting lines to compare strategies.
    """
    data = pickle.load(open('results/results_cust_all_only_strat31jan/cust_history_clust_all_only_strat.p', 'rb'))
    score = pickle.load(open('results/results_cust_all_only_strat31jan/park_score_clust_all_only_strat.p', 'rb'))

    df = pd.DataFrame(data)
    df_score = pd.DataFrame(score)

    dict = {"Random": [], "0": [], "0.25": [], "0.5": [], "0.75": [], "1": []}

    # for all strategies (random, 0, 0.25, 0.75, 1)
    for col in df:

        # every column represents a customer
        for i in df[col]:

            sums = []
            for run in i:
                sums.append(np.sum(i[run]))

            dict[str(col)].append(np.sum(sums))

    df_sum = pd.DataFrame(dict)

    total = pd.DataFrame(df_score.values*df_sum.values, columns=df_score.columns, index=df_score.index)

    data = []
    data_2 = []
    names = []

    for key in dict:
        data.append(dict[key])

    for key in total:
        data_2.append(list(total[key]))
        names.append(key)

    # plotting
    plt.xticks(np.arange(len(names))+1, names)
    plt.title("Total amount of rides", fontsize = 16)
    plt.boxplot(data)
    plt.ylabel("Amount of rides", fontsize = 14)
    plt.xlabel("Strategy", fontsize = 14)
    plt.xticks([1,2,3,4,5,6],names)
    plt.show()

    plt.title("Total waiting times", fontsize = 16)
    plt.boxplot(data_2)
    plt.ylabel("Waiting time", fontsize=14)
    plt.xlabel("Strategy", fontsize = 14)
    plt.xticks([1,2,3,4,5,6],names)
    plt.show()


def plot_efficiency_score():
    file = pickle.load(open('results/results_cust_all_only_strat31jan/eff_score_clust_all_only_strat.p', 'rb'))

    arrays = [np.array(x) for x in file["Random"]]
    means = [np.mean(k) for k in zip(*arrays)]
    arrays = [np.array(x) for x in file[0]]
    means2 = [np.mean(k) for k in zip(*arrays)]
    arrays = [np.array(x) for x in file[0.25]]
    means3 = [np.mean(k) for k in zip(*arrays)]
    arrays = [np.array(x) for x in file[0.5]]
    means4 = [np.mean(k) for k in zip(*arrays)]
    arrays = [np.array(x) for x in file[0.75]]
    means5 = [np.mean(k) for k in zip(*arrays)]
    arrays = [np.array(x) for x in file[1]]
    means6 = [np.mean(k) for k in zip(*arrays)]

    x_pos = np.arange(len(STRATEGIES))

    plt.title("Park efficiency score")
    plt.plot(means)
    plt.plot(means2)
    plt.plot(means3)
    plt.plot(means4)
    plt.plot(means5)
    plt.plot(means6)
    plt.xlabel("Timestep")
    plt.ylabel("Score")
    plt.legend(STRATEGIES)
    plt.show()
    plt.title("Park efficiency")
    plt.ylabel("Score")
    plt.bar(STRATEGIES, [np.mean(means), np.mean(means2), np.mean(means3), np.mean(means4), np.mean(means5), np.mean(means6)])
    plt.xticks(x_pos, STRATEGIES)
    plt.ylim(0.3,0.9)
    plt.show()


def plot_efficiency_score2():

    file = pickle.load(open('results_random_and_noise_8feb/eff_score_clust_main_rand_noise.p', 'rb'))
    file2 = pickle.load(open('results_random_and_noise_8feb/eff_score_clusterd_diff_strat.p', 'rb'))
    file3 = pickle.load(open('results_random_and_noise_8feb/eff_score_clusterd_only_random.p', 'rb'))

    arrays = [np.array(x) for x in file3]
    means = [np.mean(k) for k in zip(*arrays)]

    array_effscorenoise = [np.array(x) for x in file]
    means_effscorenoise = [np.mean(k) for k in zip(*array_effscorenoise)]

    array_effscore = [np.array(x) for x in file2]
    means_effscore = [np.mean(k) for k in zip(*array_effscore)]

    print(array_effscore)

    plt.title("Park efficiency score, adaptive with noise")
    plt.plot(means_effscorenoise)
    plt.plot(means)
    plt.legend(["Adaptive agents with noise", "Random"])

    plt.xlabel("Timestep")
    plt.ylabel("Score")
    plt.show()

    plt.title("Park efficiency score, adaptive")
    plt.plot(means_effscore)
    plt.plot(means)
    plt.legend(["Adaptive agents", "Random"])

    plt.xlabel("Timestep")
    plt.ylabel("Score")
    plt.show()


def plot_strategy_hist_clust():
    file = pickle.load(open('results/results_cust_all_only_strat31jan/strategy_history_clusterd_diff_strat.p', 'rb'))

    STRATEGIES = ["0.00", "0.25", "0.50", "0.75", "1.00"]
    data = {}
    for strat in STRATEGIES:
        data[strat] = []
    for line in file:

        for strat in STRATEGIES:

            # Get last value in the list
            data[strat].append(line.iloc[RUNS - 1][strat])

    x_pos = np.arange(len(STRATEGIES))
    values = data.values()
    values = list(values)

    total = []
    total.append(values[0])
    total.append(values[1])
    total.append(values[2])
    total.append(values[3])
    total.append(values[4])

    # fill with colors
    colors = ["lightgreen", "lightblue", "lightgreen", "lightblue", "lightgreen", "lightblue", "lightgreen", "lightblue", "lightgreen", "lightblue"]
    ticks = STRATEGIES
    fig, axes = plt.subplots()

    boxplot = axes.boxplot(total, patch_artist=True, widths=0.8)
    plt.xticks(x_pos + 1, STRATEGIES)
    plt.yticks(np.arange(0, 100, 20))

    colors = ['lightblue', 'lightblue', 'lightblue', "lightblue", "lightblue"]

    for patch, color in zip(boxplot['boxes'], colors):
        patch.set_facecolor(color)

    # adding horizontal grid lines
    axes.yaxis.grid(True)
    axes.set_title("Ratio of people with a specific strategy at the end of a run")
    axes.set_xlabel('Strategy')
    axes.set_ylabel('Percentage of people')
    plt.show()

    total2 = []

    total2.append(round(np.mean(values[0]), 1))
    total2.append(round(np.mean(values[1]), 1))
    total2.append(round(np.mean(values[2]), 1))
    total2.append(round(np.mean(values[3]), 1))
    total2.append(round(np.mean(values[4]), 1))

    plt.title("Ratio of strategies at end of run")
    plt.pie(total2, autopct='%1.1f%%')
    plt.legend(STRATEGIES)
    plt.show()


def plot_strategy_hist_clust2():
    file = pickle.load(open('results/results_cust_all_only_strat31jan/strategy_history_clusterd_diff_strat.p', 'rb'))

    STRATEGIES = ["0.00", "0.25", "0.50", "0.75", "1.00"]
    data = {}
    for strat in STRATEGIES:
        data[strat] = []
    for line in file:

        for strat in STRATEGIES:

            # Get last value in the list
            data[strat].append(line.iloc[RUNS - 1][strat])

    x_pos = np.arange(len(STRATEGIES))
    values = data.values()
    values = list(values)

    total = []
    total.append(values[0])
    total.append(values[1])
    total.append(values[2])
    total.append(values[3])
    total.append(values[4])

    # fill with colors
    colors = ["lightgreen", "lightblue", "lightgreen", "lightblue", "lightgreen", "lightblue", "lightgreen", "lightblue", "lightgreen", "lightblue"]
    ticks = STRATEGIES
    fig, axes = plt.subplots()

    boxplot = axes.boxplot(total, patch_artist=True, widths=0.8)
    plt.xticks(x_pos + 1, STRATEGIES)
    plt.yticks(np.arange(0, 100, 20))

    colors = ['lightblue', 'lightblue', 'lightblue', "lightblue", "lightblue"]

    for patch, color in zip(boxplot['boxes'], colors):
        patch.set_facecolor(color)

    # adding horizontal grid lines
    axes.yaxis.grid(True)
    axes.set_title("Ratio of people with a specific strategy at the end of a run")
    axes.set_xlabel('Strategy')
    axes.set_ylabel('Percentage of people')
    plt.show()

    total2 = []

    total2.append(round(np.mean(values[0]), 1))
    total2.append(round(np.mean(values[1]), 1))
    total2.append(round(np.mean(values[2]), 1))
    total2.append(round(np.mean(values[3]), 1))
    total2.append(round(np.mean(values[4]), 1))

    plt.title("Ratio of strategies at end of run")
    plt.pie(total2, autopct='%1.1f%%')
    plt.legend(STRATEGIES)
    plt.show()


def plot_eff():
    file = pickle.load(open('results/results_cust_all_only_strat31jan/eff_score_clust_all_only_strat.p', 'rb'))

    arrays = [np.array(x) for x in file["Random"]]
    means = [np.mean(k) for k in zip(*arrays)]
    arrays = [np.array(x) for x in file[0]]
    means2 = [np.mean(k) for k in zip(*arrays)]
    arrays = [np.array(x) for x in file[0.25]]
    means3 = [np.mean(k) for k in zip(*arrays)]
    arrays = [np.array(x) for x in file[0.5]]
    means4 = [np.mean(k) for k in zip(*arrays)]
    arrays = [np.array(x) for x in file[0.75]]
    means5 = [np.mean(k) for k in zip(*arrays)]
    arrays = [np.array(x) for x in file[1]]
    means6 = [np.mean(k) for k in zip(*arrays)]

    plt.title("Park efficiency score")
    plt.xlabel("Timestep")
    plt.ylabel("Score")

    plt.boxplot([means, means2, means3, means4, means5, means6])
    plt.show()


def plot_strategy_hist():
    file = pickle.load(open('results/results_cust_all_only_strat31jan/strategy_history_clust_main_rand.p', 'rb'))

    STRATEGIES = ["Random", "0.00", "0.25", "0.50", "0.75", "1.00"]
    data = {}
    for strat in STRATEGIES:
        data[strat] = []
    for line in file:

        for strat in STRATEGIES:

            # Get last value in the list
            data[strat].append(line.iloc[RUNS - 1][strat])

    STRATEGIES = ["0.00", "0.25", "0.50", "0.75", "1.00"]
    data2 = {}
    for strat in STRATEGIES:
        data2[strat] = []
    for line in file2:
        for strat in STRATEGIES:

            # Get last value in the list
            data2[strat].append(line.iloc[RUNS - 1][strat])

    x_pos = np.arange(len(STRATEGIES * 2))
    values = data.values()
    values2 = data2.values()
    values = list(values)
    values2 = list(values2)

    total = []
    total.append(values[0])
    total.append(values2[0])
    total.append(values[1])
    total.append(values2[1])
    total.append(values[2])
    total.append(values2[2])
    total.append(values[3])
    total.append(values2[3])
    total.append(values[4])
    total.append(values2[4])

    # fill with colors
    colors = ["lightgreen", "lightblue", "lightgreen", "lightblue", "lightgreen", "lightblue", "lightgreen", "lightblue", "lightgreen", "lightblue"]
    ticks = STRATEGIES
    fig, axes = plt.subplots()

    boxplot = axes.boxplot(total, patch_artist=True, widths=0.4, positions = [0.7, 1.3, 2.7, 3.3, 4.7, 5.3, 6.7, 7.3, 8.7, 9.3])
    plt.xticks(x_pos + 1, STRATEGIES)
    plt.xticks(range(1, len(ticks) * 2, 2), ticks)
    for patch, color in zip(boxplot['boxes'], colors):
        patch.set_facecolor(color)

    custom_lines = [Line2D([0], [0], color="lightgreen", lw=4),
                    Line2D([0], [0], color="lightblue", lw=4)]

    # adding horizontal grid lines
    axes.yaxis.grid(True)
    axes.set_title("Average number of people with a specific strategy, runs=65")
    axes.set_xlabel('Strategy')
    axes.set_ylabel('Number of people')
    axes.legend(custom_lines, ["Cluster", "Circle"])
    plt.show()


def plot_strategies():
    """
    Transform data and plot strategies
    """
    try:
        file = pickle.load(open('dataannemijn/strategy_history_clust_main_rand_noise.p', 'rb'))
        file = pickle.load(open('datalotte/resultaten/strategy_history_clusterd_diff_strat.p', 'rb'))
        file2 = pickle.load(open('results/results_cust_all_only_strat31jan/strategy_history_clusterd_diff_strat.p', 'rb'))
    except:
        file = pickle.load(open('../results/results_cust_all_only_strat31jan/strategy_history_clust_main_rand.p', 'rb'))
        file2 = pickle.load(open('../results/results_cust_all_only_strat31jan/strategy_history_clusterd_diff_strat.p', 'rb'))

    files = [file, file2]

    for nr in range(1):

        file = files[0]

        df = pd.DataFrame(file)
        nr_cols = len(df[0][0].columns)

        length_iter = len(df[0][0])
        length_df = len(df[0])

        if nr_cols == 5:
            means = {"0.00": [ list() for i in range(length_iter) ], "0.25": [ [] for i in range(length_iter) ], "0.50": [ [] for i in range(length_iter) ], "0.75": [ [] for i in range(length_iter) ], "1.00": [ [] for i in range(length_iter) ]}
        elif nr_cols == 6:
            means = {"0.00": [ list() for i in range(length_iter) ], "0.25": [ [] for i in range(length_iter) ], "0.50": [ [] for i in range(length_iter) ], "0.75": [ [] for i in range(length_iter) ], "1.00": [ [] for i in range(length_iter) ], "Random": [ list() for i in range(length_iter) ]}

        # loop over all datasets in df
        for i in range(length_df):

            # for all cols in dataset (0.00, 0.25, 0.50, 0.75, 1.00)
            for col in df[0][i]:

                # save data for each column in dictionary
                for k, val in enumerate(list(df[0][i][col])):

                    means[col][k].append(val)

        # colors for lines and variance ranges
        linecolors = [(0.12156862745098039, 0.4666666666666667, 0.7058823529411765, 1),\
                        (1.0, 0.4980392156862745, 0.054901960784313725, 1),\
                        (0.17254901960784313, 0.6274509803921569, 0.17254901960784313, 1),\
                        (0.8392156862745098, 0.15294117647058825, 0.1568627450980392, 1),\
                        (0.5803921568627451, 0.403921568627451, 0.7411764705882353, 1),\
                        (0.5490196078431373, 0.33725490196078434, 0.29411764705882354, 1)]
        colors = [(0.12156862745098039, 0.4666666666666667, 0.7058823529411765, 0.1),\
                        (1.0, 0.4980392156862745, 0.054901960784313725, 0.1),\
                        (0.17254901960784313, 0.6274509803921569, 0.17254901960784313, 0.1),\
                        (0.8392156862745098, 0.15294117647058825, 0.1568627450980392, 0.1),\
                        (0.5803921568627451, 0.403921568627451, 0.7411764705882353, 0.1),\
                        (0.5490196078431373, 0.33725490196078434, 0.29411764705882354, 0.1)]

        # get mean and std from data for plots
        for nr , key in enumerate(means):

            key_content = means[str(key)]

            e = []
            mean = []

            for i in range(len(key_content)):
                e.append(np.std(key_content[i]))
                means[str(key)][i] = np.mean(key_content[i])

            # plotting: with or without error ranges
            plt.errorbar(y=means[str(key)], x=list(np.arange(1,len(means[str(key)])+1)), color=linecolors[nr],yerr=e, fmt='-', ecolor=colors[nr])
            # plt.plot(means[str(key)])

    # without random condition
    if nr_cols == 5:
        plt.title("Strategy adaptation over time (N=65)", fontsize=16)
        plt.xlabel("Time (steps)", fontsize=14)
        plt.ylabel("Amount of visitors", fontsize=14)
        plt.legend(["0.00", "0.25", "0.50", "0.75", "1.00"])
        plt.savefig("strategycomparison_var_1000", dpi=300)
        plt.show()

    # with random condition
    elif nr_cols == 6:
        plt.title("Strategy adaptation over time, with noise (N=65)", fontsize=16)
        plt.xlabel("Time (steps)", fontsize=14)
        plt.ylabel("Amount of visitors", fontsize=14)
        plt.legend(["0.00", "0.25", "0.50", "0.75", "1.00", "Random"])
        plt.savefig("strategycomparison_noise_var_1000", dpi=300)
        plt.show()


def plot_compare_eff():
    """
    Transform data and plot strategies
    """
    try:
        # file = pickle.load(open('dataannemijn/eff_score_clust_main_rand_noise.p', 'rb'))
        file = pickle.load(open('datalotte/resultaten/eff_score_clusterd_diff_strat.p', 'rb'))
        file2 = pickle.load(open('dataannemijn/eff_score_clusterd_only_random.p', 'rb'))
    except:
        file = pickle.load(open('../dataannemijn/eff_score_clust_main_rand_noise.p', 'rb'))
        file2 = pickle.load(open('../dataannemijn/eff_score_clusterd_diff_strat.p', 'rb'))

    files = [file, file2]

    # for nr, file in enumerate(files):
    for nr in range(len(files)):

        file = files[nr]

        df = pd.DataFrame(file)
        nr_cols = len(df[0][0].columns)

        length_iter = len(df[0][0])
        length_df = len(df[0])

        means = [ list() for i in range(length_iter) ]

        # loop over all datasets in df
        for i in range(length_df):

            # for all cols in dataset (0.00, 0.25, 0.50, 0.75, 1.00)
            for col in df[0][i]:

                # save data for each column in dictionary
                for k, val in enumerate(list(df[0][i][col])):

                    means[k].append(val)

        # define colors for plotting lines and variance
        linecolors = [(0.9,0.5,0.2,1),(0.3,0.3,0.6,1)]
        colors = [(0.9,0.5,0.2,0.1),(0.3,0.3,0.6,0.1)]

        # save means and variance (standard deviation)
        e = []
        mean = []
        for t, key in enumerate(means):
            e.append(np.std(key))
            means[t] = np.mean(key)

        # plot with error ranges
        plt.errorbar(y=means, x=list(np.arange(1,len(means)+1)), color=linecolors[nr],yerr=e, fmt='-', ecolor=colors[nr])

        # uncomment for plotting without error ranges
        # plt.plot(means)

    # plotting
    plt.title("Adaptive park efficiency vs random (N=65)", fontsize=16)
    plt.xlabel("Time (steps)", fontsize=14)
    plt.ylabel("Efficiency score", fontsize=14)
    plt.legend(["Adaptive agents", "Random"])
    plt.savefig("Eff_var_1000", dpi=300)
    plt.show()


# UNCOMMENT Functions to use:

# plot_eff()
# plot_themepark_score()
# plot_efficiency_score2()
# plot_strategy_hist()
# plot_strategy_hist_clust()
# plot_compare_eff()
# plot_strategies()
# plot_boxplots()
