import pickle
import matplotlib.pylab as plt
import numpy as np
import seaborn as sns
sns.set()

RUNS = 520

file = pickle.load(open('all_circle_data_28/stategy_history_circle.p', 'rb'))
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
temp = []
for x in values:
    temp.append(np.mean(x))

temp = [float(i) for i in temp]
# plt.title("Mean number of people ended in a specific strategy")
# plt.xlabel("Strategy")
# plt.ylabel("Mean number of people")
# plt.xticks(x_pos, STRATEGIES)
# plt.bar(x_pos, temp)
# plt.show()

plt.boxplot(values)
plt.xticks(x_pos + 1, STRATEGIES)
plt.show()
