try:
    from .model import Themepark
except ModuleNotFoundError:
    from model import Themepark
import pickle

width = 36
height = 36
pixel_ratio = 20
theme = "circle"
strategy = "Closest_by"
cust_dict, score_dict, hapiness_dict, hist_dict, strat_dict, dict_dict = {}, {}, {}, {}, {}, {}

N_cust = 120
num_agents = 12
steps = 520
RUNS = 15
strategies = ["Random", 0, 0.25, 0.5, 0.75, 1]
adaptive = False


for run in strategies:
    cust_d, score_d, hapiness_d, hist_d, strategy_d, dict2 = [], [], [], [], [], []

    for j in range(RUNS):

        print()
        print("RUN ", j, run)
        print()

        if run == "Random":
            strategy = "Random"
        else:
            strategy = "Closest_by"

        park = Themepark(num_agents, N_cust, width, height, strategy, theme, steps, run, adaptive)

        for i in range(steps + 1):
            print("step", i)
            park.step()

        try:
            cust = pickle.load(open("data/customers.p", 'rb'))
            score = pickle.load(open("data/park_score.p", "rb"))
            hapiness = pickle.load(open("data/hapiness.p", "rb"))
            hist = pickle.load(open("data/cust_history.p", 'rb'))
            strategy_hist = pickle.load(open("data/strategy_history.p", 'rb'))
            dict2_data = pickle.load(open("data/eff_score_history.p", 'rb'))

        except:
            cust = pickle.load(open("../data/customers.p", 'rb'))
            score = pickle.load(open("../data/park_score.p", "rb"))
            hapiness = pickle.load(open("../data/hapiness.p", "rb"))
            hist = pickle.load(open("../data/cust_history.p", 'rb'))
            strategy_hist = pickle.load(open("../data/strategy_history.p", 'rb'))
            dict2_data = pickle.load(open("../data/eff_score_history.p", 'rb'))


        cust_d.append(cust)
        score_d.append(score)
        hapiness_d.append(hapiness)
        hist_d.append(hist)
        strategy_d.append(strategy_hist)
        dict2.append(dict2_data)


    cust_dict[run] = cust_d
    score_dict[run] = score_d
    hapiness_dict[run] = hapiness_d
    hist_dict[run] = hist_d
    strat_dict[run] = strategy_d
    dict_dict[run] = dict2

    # print(score_dict, hapiness_dict)
    # print(strat_dict)

try:
    pickle.dump(cust_dict, open("results/customers_circle_all_only_strat.p", 'wb'))
    pickle.dump(score_dict, open("results/park_score_circle_all_only_strat.p", "wb"))
    pickle.dump(hapiness_dict, open("results/hapiness_circle_all_only_strat.p", "wb"))
    pickle.dump(hist_dict, open("results/cust_history_circle_all_only_strat.p", 'wb'))
    pickle.dump(strat_dict, open("results/strategy_history_circle_all_only_strat.p", 'wb'))
    pickle.dump(dict_dict, open("results/eff_score_circle_all_only_strat.p", 'wb'))

except:
    pickle.dump(cust_dict, open("../results/customers_circle_all_only_strat.p", 'wb'))
    pickle.dump(score_dict, open("../results/park_score_circle_all_only_strat.p", "wb"))
    pickle.dump(hapiness_dict, open("../results/hapiness_circle_all_only_strat.p", "wb"))
    pickle.dump(hist_dict, open("../results/cust_history_circle_all_only_strat.p", 'wb'))
    pickle.dump(strat_dict, open("../results/strategy_history_circle_all_only_strat.p", 'wb'))
    pickle.dump(dict_dict, open("../results/eff_score_circle_all_only_strat.p", 'wb'))
