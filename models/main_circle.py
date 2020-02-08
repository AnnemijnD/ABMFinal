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
strategies = [0, 0.25, 0.5, 0.75, 1, "Random"]

N_cust = 120
num_agents = 12
steps = 520
RUNS = 65


cust_d, score_d, hapiness_d, hist_d, strat_d, score_ed = [], [], [], [], [],[]


for j in range(RUNS):

    print()
    print("RUN ", j)
    print()

    park = Themepark(num_agents, N_cust, width, height, strategy, theme, steps, None)

    for i in range(steps + 1):
        print("step", i)
        park.step()

    cust = pickle.load(open("../data/customers.p", 'rb'))
    score = pickle.load(open("../data/park_score.p", "rb"))
    hapiness = pickle.load(open("../data/hapiness.p", "rb"))
    hist = pickle.load(open("../data/cust_history.p", 'rb'))
    strategy_hist = pickle.load(open("../data/stategy_history.p", 'rb'))

    cust_d.append(cust)
    score_d.append(score)
    hapiness_d.append(hapiness)
    hist_d.append(hist)
    strat_d.append(strategy_hist)

    print(score_d)
    print(hapiness_d)
    print(strat_d)

pickle.dump(cust_d, open("../data/customers_circle.p", 'wb'))
pickle.dump(score_d, open("../data/park_score_circle.p", "wb"))
pickle.dump(hapiness_d, open("../data/hapiness_circle.p", "wb"))
pickle.dump(hist_d, open("../data/cust_history_circle.p", 'wb'))
pickle.dump(strat_d, open("../data/stategy_history_circle.p", 'wb'))
