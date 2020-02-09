from mesa import Agent
import random
import math
try:
    from .route import Route
except:
    from route import Route
import numpy as np
import math



class Customer(Agent):
    def __init__(self, unique_id, model, pos, strategy, weight, adaptive):
        super().__init__(unique_id, model)

        """
        Args:
        id (int): a unique id to represent the agent
        model (Themepark): the model to link the agent to
        pos (tuple(int,int)): the position of the agent (x,y)
        strategy (str): indicates if agent uses a strategy or behaves randomly
        weight (float): float indicating the weight given to distance and queuetime
        adaptive (bool): if true, agent can switch strategies through run
        """
        self.pos = pos
        self.model = model
        self.current_a = None
        self.strategy = strategy
        self.history = self.make_history()
        self.weight = weight
        if self.weight == "Random_test_4":
            self.strategy = "Random_test_4"
        self.adaptive = adaptive
        self.all_strategies =  [x for x in self.model.strategies if x != 'Random_test_4']

        if self.strategy == 'Random' or self.strategy == "Random_test_4":
            self.destination = random.choice(self.model.positions)
            while self.destination is self.pos:
                self.destination = random.choice(self.model.positions)

        if self.strategy == 'Closest_by':
            self.destination = self.use_strategy().pos

        self.waitingtime = None
        self.waiting = False
        self.total_ever_waited = 0
        self.nmbr_attractions = 0
        self.waited_period = 0
        self.in_attraction = False
        self.in_attraction_list = []
        self.prediction_strategies = self.prediction_all_strategies()
        self.strategy_swap_hist = 0

    def make_history(self):
        """
        This method provides the framework for the customer attraction history
        """

        history = {}
        attractions = self.model.attractions
        for attraction in range(len(attractions)):
            history[attractions[attraction]] = 0

        return history

    def penalty(self, current_attraction):
        """
        This method calculates and returns a penalty for attractions that were visited more
        often than other attractions.
        Args:
        current_attraction (Attraction): the attraction object the method calculates
                                         a penalty for.
        """


        total_difference_sum = 0

        if current_attraction == 0:
            return 0

        # calculates the difference between how much the current attraction was visited
        # and how much all other attractions were visited
        for i in range(len(self.model.attractions.values())):
            attraction = self.model.attractions[i]

            difference = self.history[current_attraction] - self.history[attraction]

            # update the total difference
            total_difference_sum += difference

        if total_difference_sum < 0:
            total_difference_sum = 0

        # calculates penalty by multiplying with a determinsitc value
        penalty = (total_difference_sum * self.model.penalty_per)/100

        return penalty

    def move(self):
        '''
        This method should get the neighbouring cells (Moore's neighbourhood),
        select one closest to the destination, and move the agent there.
        '''

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            radius=1,
            include_center=False
        )

        # chooses random step
        temp = random.choice(possible_steps)

        # Loop over every possible step to get fastest step
        for step in possible_steps:

            # check if step is closer to destination
            if (abs(step[0] - self.destination[0]) < abs(temp[0] - self.destination[0]) or
               abs(step[1] - self.destination[1]) < abs(temp[1] - self.destination[1])):
               temp = step

        new_position = temp

        if new_position == self.destination and self.waiting is False:
            self.model.grid.move_agent(self, new_position)

            # Get object of current attraction
            attractions = self.model.get_attractions()
            for attraction in attractions:
                if attraction.pos == new_position:
                    current_a = attraction
            self.current_a = current_a

            self.set_waiting_time()
            self.waiting = True

        # Extra check to see if agent is at destination
        if self.check_move() is True:
            self.model.grid.move_agent(self, new_position)

    def check_move(self):
        """ Checks if a move can be done, given a new position."""


        if self.waitingtime is not None:

            # set in ride to true false
            if self.current_a is not None:
                if self.waited_period == self.waitingtime - self.current_a.attraction_duration:
                    self.in_attraction = True

            # CHANGE DIRECTION if waitingtime is met
            if self.waitingtime <= self.waited_period:

                # when attraction is left set self.attraction to false
                self.in_attraction = False

                # Update goals and attraction
                for attraction in self.model.get_attractions():
                    if attraction.pos == self.pos:
                        if attraction.N_current_cust > 0:
                            attraction.N_current_cust -= 1
                            self.model.attraction_history[attraction][self.model.totalTOTAL] -=1

            # if agent is next in line
            if self.waitingtime == self.waited_period:

                if self.current_a is not None:
                    self.history[self.current_a] += 1

                    # Only update when adaptive strategy is on
                    if self.adaptive is True:
                        if self.strategy is not "Random":
                            if self.strategy is not "Random_test_4":
                                self.update_strategy()

                # increment number of rides taken of attraction
                # if self.current_a is not None:
                self.current_a.rides_taken += 1

                # increment number of rides taken of customer
                self.nmbr_attractions += 1
                self.total_ever_waited += self.waited_period
                self.waited_period = 0

                # set current attraction back to None when customer leaves.
                self.current_a = None

                # decide on new destination
                if self.strategy == "Closest_by":
                    self.destination = self.use_strategy().pos
                elif self.strategy == 'Random' or self.strategy == "Random_test_4":
                    self.destination = random.choice(self.model.positions)
                    while self.destination is self.pos:
                        self.destination = random.choice(self.model.positions)
                self.waiting = False
                self.waited_period = 0

        if self.pos == self.destination:

            # Check which attraction
            attractions = self.model.get_attractions()
            for attraction in attractions:
                if attraction.pos == self.pos:
                    self.current_a = attraction

            # self.current_a. += 1
            self.waited_period += 1

        if self.waiting is False:
            return True
        return False

    def set_waiting_time(self):
        '''
        This method calculates the waiting time of the customer based on the
        number of customers in line, and the duration of the attraction
        '''
        attractions = self.model.get_attractions()
        attraction = None
        for i in attractions:
            if self.pos == i.pos:
                attraction = i
                break

        # update waitingtime of attraction
        attraction.N_current_cust += 1

        self.model.attraction_history[attraction][self.model.totalTOTAL] +=1
        attraction.calculate_waiting_time()

        # add waiting time to agent
        self.waitingtime = attraction.current_waitingtime

    def get_walking_distances(self):
        """
        Returns dictionary of attraction-ids with their distances as values.
        Function uses pythagoras formula.
        """
        attractions = self.model.get_attractions()

        distances = {}
        for attraction in attractions:

            # Stelling van pythagoras
            p1, p2 = self.pos, attraction.pos
            dist = math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))
            distances[attraction.unique_id] = dist

        # Sort by shortest distance
        indexes = []
        {indexes.append(k): v for k, v in sorted(distances.items(), key=lambda item: item[1])}
        return distances

    def get_waiting_lines(self):
        """
        Returns dictionary of attracion-ids with their waiting lines as values.
        """
        people = self.model.calculate_people_sorted()
        return people

    def update_strategy(self):
        """
        Updates the strategy by evaluating the attractions chosen by all other
        strategies. The strategy that would have resulted in the earliest access
        to a ride is chosen as the next strategy. Only used if adaptive = True.
        """

        # dictionary of strategies that were better than the current
        strategy_ranking = {}
        queues = self.get_waiting_lines()
        chosen_strategy = self.weight
        current_walking_distance = self.prediction_strategies[chosen_strategy][1]
        current_arrival_time = math.ceil(self.prediction_strategies[chosen_strategy][2])

        if self.current_a is not None:

            for strategy in self.prediction_strategies.keys():

                # does not need compare the current strategy to itself
                if strategy == chosen_strategy:
                    continue

                attraction = self.prediction_strategies[strategy][0]
                arrival_time = math.ceil(self.prediction_strategies[strategy][2])
                walking_distance = self.prediction_strategies[strategy][1]

                # if the strategy predicted the same attraction, the old strategy
                # is prefered
                if attraction == self.current_a:
                    continue

                # if the arrival time at the predicted attraction isn't in the future
                if math.ceil(arrival_time) < self.model.totalTOTAL:

                    queue_at_arrival = self.model.attraction_history[attraction][math.ceil(arrival_time)]

                    # if the ride would have been finished earlier, add this strategy to ranking
                    if arrival_time + queue_at_arrival + attraction.attraction_duration < self.model.totalTOTAL:

                        strategy_ranking[strategy] = arrival_time + queue_at_arrival

            # choose the strategy with the best time
            if len(strategy_ranking.values()) > 0:
                minval = min(strategy_ranking.values())
                res = [k for k, v in strategy_ranking.items() if v == minval]
                if len(res) is 1:
                    best_strat = res[0]
                else:

                    # if two strategies had the same outcome, choose randomly
                    best_strat = random.choice(res)
                self.weight = best_strat

    def step(self):
        """
        This method should move the customer using the `random_move()` method.
        """

        # updates the data on the attraction occupation
        if self.in_attraction is True:
            self.in_attraction_list.append(1)
        else:
            self.in_attraction_list.append(0)

        self.move()

    def use_strategy(self):
        """
        This method returns the attraction predicted by the current strategy of
        the customer. Adds a deterministic penalty per attraction based
        on the penalty method.
        """

        # add walking times
        predictions = self.get_walking_distances()

        # add waitingtimes
        waiting_times = self.get_waiting_lines()

        # make prediction based on the current strategy for all attractions
        for i in range(len(predictions.keys())):
            predictions[i] = predictions[i] * (1 - self.weight) + waiting_times[i] * self.weight

        # use a fraction of the attraction with the highest cost as a penalty
        maxval = max(predictions.values())
        for attraction_nr in predictions:
            penalty = self.penalty(self.model.attractions[attraction_nr])
            predictions[attraction_nr] = predictions[attraction_nr] + maxval * penalty

        # choose the attraction with the lowest cost
        minval = min(predictions.values())
        res = [k for k, v in predictions.items() if v == minval]
        if len(res) is 1:
            predicted_attraction = res[0]
        else:

            # if attractions have the same cost, choose one randomly
            predicted_attraction = random.choice(res)

        attraction_object = self.model.get_attractions()[predicted_attraction]

        # make predicitons for all strategies
        self.prediction_strategies = self.prediction_all_strategies()

        return self.model.attractions[predicted_attraction]

    def prediction_all_strategies(self):
        """
        Makes a prediction for all possible strategies.
        Returns a dictionary with the strategies as keys and the attractions,
        predictions and arrival times as value
        """

        prediction_per_strategy = {}

        # add walking distances
        predictions = self.get_walking_distances()

        # add waitingtimes
        waiting_times = self.get_waiting_lines()

        # make a prediction for all srategies
        for weight in self.all_strategies:

            # make prediction based on the current strategy for all attractions
            for i in range(len(predictions.keys())):

                if self.weight is None:
                    predictions[i] = predictions[i] + waiting_times[i]
                else:
                    predictions[i] = predictions[i] * (1 - weight) + waiting_times[i] * weight

            # use a fraction of the attraction with the highest cost as a penalty
            maxval = max(predictions.values())
            for attraction_nr in predictions:
                penalty = self.penalty(self.model.attractions[attraction_nr])

                predictions[attraction_nr] = predictions[attraction_nr] + maxval * penalty

            # choose the attraction with the lowest cost
            minval = min(predictions.values())
            res = [k for k, v in predictions.items() if v == minval]
            if len(res) is 1:
                predicted_attraction = res[0]
            else:

                # if attractions have the same cost, choose randomly
                predicted_attraction = random.choice(res)

            attraction_object = self.model.get_attractions()[predicted_attraction]
            predictions = self.get_walking_distances()
            arrival_time = self.model.totalTOTAL + predictions[predicted_attraction]

            # add to dictionary
            prediction_per_strategy[weight] = [self.model.attractions[predicted_attraction], predictions[predicted_attraction],
                                                arrival_time]
        return prediction_per_strategy
