from mesa import Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
import random
import pickle
import numpy as np
from .customer import Customer
from .attraction import Attraction


FRACTION_RANDOM = 1/6
WIDTH = 36
HEIGHT = 36
RADIUS = int(WIDTH/2)
NUM_OBSTACLES = 0
mid_point = (int(WIDTH/2), int(HEIGHT/2))
PENALTY_PERCENTAGE = 5
STRATEGIES = [0.0, 0.25, 0.5, 0.75, 1.0]

# HARDCODED COORDINATES for cluster theme:
xlist, ylist, positions = [12, 21, 26, 11, 9, 25, 25, 26, 20, 12, 11, 21], [17, 26, 13, 17, 18, 12, 11, 12, 28, 16, 18, 29], [(12, 17), (21, 26), (26, 13), (11, 17), (9, 18), (25, 12), (25, 11), (26, 12), (20, 28), (12, 16), (11, 18), (21, 29)]


class Themepark(Model):
    def __init__(self, N_attr, N_cust, width, height, strategy, theme, max_time, weight, adaptive):
        self.theme = theme
        self.max_time = max_time
        self.N_attr = N_attr
        self.penalty_per = PENALTY_PERCENTAGE
        self.weight = weight
        self.adaptive = adaptive
        self.strategies = STRATEGIES
        self.x_list, self.y_list, self.positions = xlist, ylist, positions
        self.happinesses = []
        self.N_attr = N_attr    # num of attraction agents
        self.N_cust = N_cust    # num of customer agents
        self.width = width
        self.height = height
        self.total_steps = 0
        self.cust_ids = N_cust
        self.strategy = strategy
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = BaseScheduler(self)
        self.schedule_Attraction = BaseScheduler(self)
        self.schedule_Customer = BaseScheduler(self)
        self.totalTOTAL = 0
        self.attractions = self.make_attractions()
        self.attraction_history = self.make_attr_hist()
        self.running = True
        self.data_dict = {}
        self.hist_random_strat = []
        self.hist_close_strat = []
        self.all_rides_list = []
        self.strategy_composition = self.make_strategy_composition()
        self.customers = self.add_customers(self.N_cust)
        self.park_score = []

        for attraction in self.get_attractions():
            self.data_dict[attraction.unique_id] = ({
                               "id": attraction.unique_id,
                               "length": attraction.attraction_duration,
                               "waiting_list": []})

        if len(self.strategies) == 6:
            self.datacollector = DataCollector(

                {"Random": lambda m: self.strategy_counter(self.strategies[0]),
                "0.00": lambda m: self.strategy_counter(self.strategies[1]),
                "0.25": lambda m: self.strategy_counter(self.strategies[2]),
                "0.50": lambda m: self.strategy_counter(self.strategies[3]),
                "0.75": lambda m: self.strategy_counter(self.strategies[4]),
                "1.00": lambda m: self.strategy_counter(self.strategies[5]),
                })
        else:
            self.datacollector = DataCollector(
                {"0.00": lambda m: self.strategy_counter(self.strategies[0]),
                "0.25": lambda m: self.strategy_counter(self.strategies[1]),
                "0.50": lambda m: self.strategy_counter(self.strategies[2]),
                "0.75": lambda m: self.strategy_counter(self.strategies[3]),
                "1.00": lambda m: self.strategy_counter(self.strategies[4]),
                })

        self.datacollector2 = DataCollector(
            {"score": lambda m: self.make_score()})


    def make_score(self):
        """
        Calculate a score for the enire theme park.
        """

        ideal = {}
        cust_in_row = 0
        for i in range(len(self.get_attractions())):
            ideal[i] = self.N_cust/self.N_attr
            cust_in_row += self.get_attractions()[i].N_current_cust

        tot_difference = 0
        for i in range(len(self.get_attractions())):

            difference = abs(cust_in_row/self.N_attr - self.get_attractions()[i].N_current_cust)
            tot_difference += difference

        fraction_not_right = (tot_difference/self.N_cust)
        return abs(1-(fraction_not_right)) * cust_in_row/self.N_cust

    def make_attr_hist(self):
        """
        Make history of attractions that are visited for each customer.
        """
        attraction_history = {}
        for attraction in self.get_attractions():

            attraction_history[attraction] = [0] * (self.max_time + 1)
        return attraction_history

    def strategy_counter(self, strategy):
        """
        Input is a strategy, for example "0.25" or "Random", output is
        the number of strategies are adopted at a current time step.
        """
        for attraction_pos in self.positions:
            counter = 0
            for agent in self.customers:
                if agent.weight == strategy:
                    counter += 1
        return counter

    def make_strategy_composition(self):
        """
        Make a composition of all strategies over the entire theme park.
        """
        if self.strategy == "Random_test_4":
            self.strategies = ["Random_test_4", 0.0, 0.25, 0.50, 0.75, 1.0]
            dict = {self.strategies[0]: 1/6, self.strategies[1]: 0.20, self.strategies[2]: 0.20,
                    self.strategies[3]: 0.20, self.strategies[4]: 0.20, self.strategies[5]: 0.20}

            composition_list = []
            for i in range(len(self.strategies)):
                if i == 0:
                    dict[self.strategies[i]] = FRACTION_RANDOM
                    continue
                else:
                    composition_list.append(random.randint(0,100))
            sum_comp = sum(composition_list)
            sum_comp = sum_comp - sum_comp * FRACTION_RANDOM
            for i in range(len(self.strategies)):
                if i == 0:
                    continue
                else:
                    dict[self.strategies[i]] = composition_list[i-1] / sum_comp

        # Runs without a random strategy
        else:
            dict = {self.strategies[0]: 0.20, self.strategies[1]:0.20, self.strategies[2]:0.20,
                    self.strategies[3]:0.20, self.strategies[4]:0.20}

            composition_list = []
            for i in range(len(self.strategies)):

                composition_list.append(random.randint(0, 100))

            sum_comp = sum(composition_list)

            sum_comp = sum_comp
            for i in range(len(self.strategies)):

                dict[self.strategies[i]] = composition_list[i-1] / sum_comp

        return dict

    def make_attractions(self):
        """
        Initialize attractions on fixed positions, defined in the global
        variables x_list and y_list.
        """

        attractions = {}
        for i in range(self.N_attr):

            pos = (self.x_list[i], self.y_list[i])
            if self.grid.is_cell_empty(pos):
                a = Attraction(i, self, pos, str(i), self.N_cust, self.weight)
                attractions[i] = a

                self.schedule_Attraction.add(a)
                self.grid.place_agent(a, pos)
        return attractions

    def get_attractions(self):
        """
        Return a list with all attractions.
        """
        agents = self.grid.get_neighbors(
            mid_point,
            moore=True,
            radius=RADIUS,
            include_center=True)

        attractions = []
        for agent in agents:
            if type(agent) == Attraction:
                attractions.append(agent)

        return attractions

    def add_customers(self, N_cust, added=False):
        """ Initialize customers on random positions."""

        weights_list = []

        # Adaptive strategy
        if self.adaptive is True:

            # Decide weights for every customer
            for j in self.strategy_composition.keys():
                for i in range(round(N_cust*self.strategy_composition[j])):
                    weights_list.append(j)

            # Add weights for the random strategy
            if len(weights_list) < self.N_cust:
                rand = random.choice(self.strategies)
                weights_list.append(rand)
            elif len(weights_list) > self.N_cust:
                rand = random.choice(weights_list)
                weights_list.remove(rand)

        else:
            if self.strategy is not "Random":
                for i in range(round(N_cust)):
                    weights_list.append(self.weight)

        cust_list = []
        for i in range(N_cust):

            # Get random location within grid height and width
            pos_temp = [random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1)]
            rand_x, rand_y = pos_temp[0], pos_temp[1]
            pos = (rand_x, rand_y)

            if added is True:
                i = self.cust_ids
            if self.strategy == "Random_test_4":
                if weights_list[i] == "Random_test_4":
                    strategy = "Random_test_4"
                else:
                    strategy = "Closest_by"
            else:
                strategy = self.strategy

            if weights_list == []:
                weight = None
            else:
                weight = weights_list[i]
            a = Customer(i, self, pos, self.positions, strategy, weight, self.adaptive)
            self.schedule_Customer.add(a)
            self.grid.place_agent(a, pos)
            cust_list.append(a)

        return cust_list

    def calculate_people(self):
        """Calculate how many customers are in which attraction."""

        counter_total = {}

        for attraction_pos in self.positions:

            agents = self.grid.get_neighbors(
                attraction_pos,
                moore=True,
                radius=0,
                include_center=True
            )

            counter = 0
            for agent in agents:
                if type(agent) is Customer:
                    counter += 1
                else:
                    attraction = agent

            attraction.N_current_cust = counter
            counter_total[attraction.unique_id] = counter

        return list(counter_total.values())

    def calc_waiting_time(self):
        """
        Return a dictionary of watingtimes for every attraction
        """
        counter_total = {}

        attractions = self.get_attractions()
        for attraction in attractions:

            counter_total[attraction.unique_id] = attraction.current_waitingtime

        return counter_total


    def calculate_people_sorted(self):
        """
        Calculate how many customers are in which attraction.
        Returns a SORTED LIST.
        For example: indexes = [3, 2, 5, 1, 4]
        indicates that attraction3 has the least people waiting.
        """

        counter_total = {}

        for attraction_pos in self.positions:

            agents = self.grid.get_neighbors(
                attraction_pos,
                moore=True,
                radius=0,
                include_center=True
            )

            counter = 0
            for agent in agents:
                if type(agent) is Customer:
                    counter += 1
                else:
                    attraction = agent

            attraction.N_current_cust = counter
            self.attraction_history[attraction][self.totalTOTAL] = counter
            counter_total[attraction.unique_id] = counter
        return counter_total

    def get_strategy_history(self):
        """ Update history with how many customers chose which strategy """

        customers = self.get_customers()
        randomstrat, closebystrat = 0, 0

        for customer in customers:
            if customer.strategy == "Random" or customer.strategy == "Random_test_4":
                randomstrat += 1
            elif customer.strategy == "Closest_by":
                closebystrat += 1

        self.hist_random_strat.append(randomstrat)
        self.hist_close_strat.append(closebystrat)

    def get_customers(self):
        """Return a list of all customers in the theme park."""
        agents = self.grid.get_neighbors(
            mid_point,
            moore=True,
            radius=RADIUS,
            include_center=True)

        customers = []

        # Count customer agents
        for agent in agents:
            if type(agent) == Customer:
                customers.append(agent)
        return customers

    def get_data_customers(self):
        """ Return dictionary with data of customers """

        data = {}
        agents = self.grid.get_neighbors(
            mid_point,
            moore=True,
            radius=RADIUS,
            include_center=True)

        for agent in agents:
            if type(agent) is Customer:
                data[agent.unique_id] = {
                "totalwaited": agent.total_ever_waited,
                "visited_attractions": agent.nmbr_attractions,
                "strategy": agent.strategy,
                "swapped_strat": agent.strategy_swap_hist
                }
        return data

    def calc_hapiness(self):
        """
        Calculate mean hapiness of all customers, based on:

        - How many rides were taken
        - Number of times in the same attraction
        - Total waiting time
        """
        customers = self.get_customers()
        scores = []

        for customer in customers:
            history = customer.history
            values = list(history.values())
            total_rides = sum(values)

            if total_rides != 0:
                scores.append(total_rides / self.N_attr - self.totalTOTAL / customer.total_ever_waited)
            else:
                return None

        scores = np.interp(scores, (min(scores), max(scores)), (1, 10))
        return np.mean(scores)

    def get_history_list(self):
        """
        Return a dictionary of the history of visited attraction for
        each customer.
        """

        customers = self.get_customers()
        histories = {}

        for customer in customers:
            history = customer.history
            values = list(history.values())
            histories[customer.unique_id] = values
        return histories

    def final(self):
        """ Return and save data at the end of the run."""

        hist_list = []
        agents = self.grid.get_neighbors(
            mid_point,
            moore=True,
            radius=RADIUS,
            include_center=True)
        attractions = self.get_attractions()

        # Make a list for the fraction of occupied rides at all time steps
        self.all_rides_list = [0] * len(attractions[0].in_attraction_list)
        for attraction in attractions:
            for i in range(len(attraction.in_attraction_list)):
                self.all_rides_list[i] += attraction.in_attraction_list[i]
        for i in range(len(self.all_rides_list)):
            self.all_rides_list[i] /= self.N_attr

        cust_data = self.get_data_customers()
        for agent in agents:
            if type(agent) is Customer:
                sum_attr = sum(agent.history.values())
                if sum_attr > 0:
                    hist_list.append(agent.strategy_swap_hist)
                else:
                    hist_list.append(agent.strategy_swap_hist)

        histories = self.get_history_list()

        # save data
        try:
            pickle.dump(self.datacollector.get_model_vars_dataframe(), open("../data/strategy_history.p", 'wb'))
            pickle.dump(self.datacollector2.get_model_vars_dataframe(), open("../data/eff_score_history.p", 'wb'))
            pickle.dump(cust_data, open("../data/customers.p", 'wb'))
            pickle.dump(self.park_score[-1], open("../data/park_score.p", "wb"))
            pickle.dump(self.happinesses, open("../data/hapiness.p", "wb"))
            pickle.dump(histories, open("../data/cust_history.p", 'wb'))
            pickle.dump(self.all_rides_list, open("../data/all_rides.p", "wb"))
        except:
            pickle.dump(self.datacollector.get_model_vars_dataframe(), open("data/strategy_history.p", 'wb'))
            pickle.dump(self.datacollector2.get_model_vars_dataframe(), open("data/eff_score_history.p", 'wb'))
            pickle.dump(cust_data, open("data/customers.p", 'wb'))
            pickle.dump(self.park_score[-1], open("data/park_score.p", "wb"))
            pickle.dump(self.happinesses, open("data/hapiness.p", "wb"))
            pickle.dump(histories, open("data/cust_history.p", 'wb'))
            pickle.dump(self.all_rides_list, open("data/all_rides.p", "wb"))

        print()
        print("RUN HAS ENDED")
        print()


    def save_data(self):
        """Save data of all attractions and customers."""

        # Get info
        waitinglines = self.calc_waiting_time()

        for i in range(len(self.attractions)):
            self.data_dict[i]["waiting_list"].append(waitinglines.get(i))

        self.park_score.append(sum(waitinglines.values()))
        self.happinesses.append(self.calc_hapiness())

    def step(self):
        """Advance the model by one step."""

        if self.totalTOTAL < self.max_time:
            self.totalTOTAL += 1
            self.schedule.step()

            # Collect data for every step
            self.datacollector.collect(self)
            self.datacollector2.collect(self)

            # Step for both attraction and customer
            self.schedule_Attraction.step()
            self.schedule_Customer.step()

            self.total_steps += 1

            # Save data and update strategy history
            self.save_data()
            self.get_strategy_history()

        else:
            for key in self.attraction_history.keys():
                y = self.attraction_history[key]
                x = list(range(0, self.max_time))
            self.final()
