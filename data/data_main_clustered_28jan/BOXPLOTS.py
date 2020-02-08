import sys
import os
sys.path.insert(0, 'finalresults')
import numpy as np
import pandas as pd
from ast import literal_eval
import json
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import scipy.stats

enemies = ["enemy1", "enemy4", "enemy6"]

total_boxplot = []
total_boxplot = []
total_islandFalse = []
total_islandTrue = []

# loop through files and open them
Islandbools = ["islandFalse", "islandTrue"]
for enemy in enemies:
    boxplot_islandFalse = []
    boxplot_islandTrue = []
    for Islandbool in Islandbools:
        foldername = "boxplots/" + enemy

        if not os.path.exists(foldername):
            os.makedirs(foldername)

        for run in range(10):
            run = str(run)
            if Islandbool == "islandFalse":
                period = "period0"
            else:
                    period = "period50"
            fileName = enemy + "_epochs100_individuals60_"+ Islandbool + "_" + period + "_run"+ run

            try:
                f = open('final_schone_data/'+fileName +'/history.txt','r')
                a = [" array(", ")", ]
                lst = []
                for line in f:
                    for word in a:
                        if word in line:
                            line = line.replace(word,'')
                    lst.append(line)
                f.close()
                f = open('final_schone_data/'+fileName +'/history.txt','w')
                for line in lst:
                    f.write(line)
                f.close()

                with open('final_schone_data/'+fileName +'/history.txt') as tweetfile:
                    dictionary = literal_eval(tweetfile.read())
                if Islandbool == "islandTrue":
                    boxplot_islandTrue.append(max(dictionary["best_grade"]))
                else:
                    boxplot_islandFalse.append(max(dictionary["best_grade"]))
            except:
                None

    total_boxplot.append(boxplot_islandFalse)
    total_boxplot.append(boxplot_islandTrue)
    total_islandTrue.append(boxplot_islandTrue)
    total_islandFalse.append(boxplot_islandFalse)

all_data = total_boxplot
print(total_boxplot)
labels = ['CGA', 'AA', 'CGA', 'AA', 'CGA', 'AA']

fig, axes = plt.subplots()

# rectangular box plot
bplot1 = axes.boxplot(all_data,
                         vert=True,  # vertical box alignment
                         patch_artist=True,  # fill with color
                         labels=labels)  # will be used to label x-ticks
axes.set_title('Best fitness-scores with different initialization parameters (n=10)')

# fill with colors
colors = ["lightgreen", "lightgreen", "lightblue", "lightblue", "pink", "pink"]

for patch, color in zip(bplot1['boxes'], colors):
    patch.set_facecolor(color)

# adding horizontal grid lines
axes.yaxis.grid(True)
axes.set_xlabel('Initialized population')
axes.set_ylabel('Fitness score')

custom_lines = [Line2D([0], [0], color="lightgreen", lw=4),
                Line2D([0], [0], color="lightblue", lw=4),
                Line2D([0], [0], color="pink", lw=4)]

axes.legend(custom_lines,['Enemy 1', 'Enemy 4', 'Enemy 6'], loc='lower right')
plt.show()

# Statistical analyses
# Shapiro test
P_values = []
for result in total_islandFalse:
    P_values.append(scipy.stats.shapiro(result))

# print(f"P_values ={P_values}")

# Mann-Whitney U-test
p_valuesmwu = []
fake_data = [[8, 1, 8, 3, 4, 5, 6, 7, 8, 9],[8, 8, 82, 83, 84, 85, 86, 87, 88, 99],[80, 81, 82, 83, 84, 85, 86, 87, 88, 99]]
# for i in range(len(total_islandFalse)):
    # print(resultF)

# i = 0, 1, 2 -> Enemy1, 4, 6
i = 2
T = np.asarray(total_islandTrue[i])
F = np.asarray(total_islandFalse[i])

p_valuesmwu.append((scipy.stats.mannwhitneyu(T, F, use_continuity=True)))
p = scipy.stats.mannwhitneyu(T, F, use_continuity=True, alternative="greate")[1]
alpha = 0.05
# print(1-p)
if p > alpha:
	print('Same distribution (fail to reject H0)')
else:
	print('With Island better fitness (reject H0)')
