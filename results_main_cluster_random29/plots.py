import pickle
import matplotlib.pyplot as plt
from statistics import mean

"""
Assumes following datatypes for results:

Agents:         1. List of integers: number of visited attractions
                2. List of integers: total time spend waiting during run

Attractions:    1. [id, duur ritje, locatie, [aantal customers], [duur wachtrij]]
"""

def histogram_attractions():
    results = pickle.load(open('../data/attractions2.p', 'rb'))
    avg_res = []
    leg =[]
    fig, ax = plt.subplots()

    for i in range(len(results[0]["waiting_list"])):
        temp = []
        for result in results:
            temp.append(results[result]["waiting_list"][i])
        avg_res.append(mean(temp))
        temp.clear()

    for result in results:
        ax.plot(results[result]["waiting_list"])
        leg.append("Attraction id " + str(results[result]["id"]))

    ax.plot(avg_res,linewidth=4, color='black')


    ax.set(xlabel='timepoints (t)', ylabel='length of waiting line (l)',
            title='Waiting lines for attractions')

    plt.savefig('histogram_closest.png')
    plt.show()

def boxplot_visitors():

    results = pickle.load(open('../data/customers2.p', 'rb'))
    waitingtime = []
    visited_attractions = []
    for result in results:
        print(results[result])
        waitingtime.append(results[result]["totalwaited"])
        visited_attractions.append(results[result]["visited_attractions"])
    fig1, ax1 = plt.subplots()
    ax1.set_title('Visitor data')
    ax1.boxplot([waitingtime,visited_attractions])
    # ax1.legend(["Total time waited", "Nr of visited attractions"])
    plt.xticks([1, 2], ["Total time waited", "Nr of visited attractions"])

    plt.savefig('boxplot_closest.png')
    plt.show()

if __name__ == "__main__":
    histogram_attractions()
    boxplot_visitors()
