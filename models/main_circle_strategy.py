from mesa import Model, Agent
try:
    from .model import Themepark
except ModuleNotFoundError:
    from model import Themepark
import pickle

width = 36
height = 36
N_cust = 120
pixel_ratio = 20
num_agents = 12
theme = "circle"
strategy = "Closest_by"
steps = 520
RUNS = 65
strategies = [0, 0.25, 0.5, 0.75, 1]
adaptive = True


cust_d, score_d, hapiness_d, hist_d, strategy_d = [], [], [], [], []

for run in range(RUNS):
    print("RUN ", run)
    park = Themepark(num_agents, N_cust, width, height, strategy, theme, steps, strategies, adaptive)

    for i in range(steps + 1):
        print("step", i)
        park.step()

    print("Number of run:", run)

    try:
        cust = pickle.load(open("data/customers.p", 'rb'))
        score = pickle.load(open("data/park_score.p", "rb"))
        hapiness = pickle.load(open("data/hapiness.p", "rb"))
        hist = pickle.load(open("data/cust_history.p", 'rb'))
        strategy_hist = pickle.load(open("data/strategy_history.p", 'rb'))
    except:
        cust = pickle.load(open("../data/customers.p", 'rb'))
        score = pickle.load(open("../data/park_score.p", "rb"))
        hapiness = pickle.load(open("../data/hapiness.p", "rb"))
        hist = pickle.load(open("../data/cust_history.p", 'rb'))
        strategy_hist = pickle.load(open("../data/strategy_history.p", 'rb'))

    cust_d.append(cust)
    score_d.append(score)
    hapiness_d.append(hapiness)
    hist_d.append(hist)
    strategy_d.append(strategy_hist)
    print(strategy_d)

    # Tussendoor opslaan
    try:
        pickle.dump(cust_d, open("results/customers_clust_main_strat.p", 'wb'))
        pickle.dump(score_d, open("results/park_score_clust_main_strat.p", "wb"))
        pickle.dump(hapiness_d, open("results/hapiness_clust_main_strat.p", "wb"))
        pickle.dump(hist_d, open("results/cust_history_clust_main_strat.p", 'wb'))
        pickle.dump(strategy_d, open("results/strategy_history_clust_main_strat.p", 'wb'))
    except:
        pickle.dump(cust_d, open("../results/customers_clust_main_strat.p", 'wb'))
        pickle.dump(score_d, open("../results/park_score_clust_main_strat.p", "wb"))
        pickle.dump(hapiness_d, open("../results/hapiness_clust_main_strat.p", "wb"))
        pickle.dump(hist_d, open("../results/cust_history_clust_main_strat.p", 'wb'))
        pickle.dump(strategy_d, open("../results/strategy_history_clust_main_strat.p", 'wb'))
