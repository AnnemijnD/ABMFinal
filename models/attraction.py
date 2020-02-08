from mesa import Agent
import random
try:
    from .route import get_attraction_coordinates, Route
except:
    from route import get_attraction_coordinates, Route
WIDTH = 36
HEIGHT = 36
RADIUS = 15
NUM_OBSTACLES = 80
MEMORY = 5


class Attraction(Agent):
    def __init__(self, unique_id, model, pos, name, N_cust, weight):
        super().__init__(unique_id, model)
        self.name = name
        self.pos = pos
        self.model = model
        self.attraction_duration = 10
        self.current_waitingtime = 0
        self.N_current_cust = 0
        self.cust_in_attr = 0
        self.cust_in_line = 0
        self.memory = []
        self.ride_time = 0
        self.rides_taken = 0
        self.in_attraction_list = []

    def calculate_waiting_time(self):
        '''
        Calculates and updates current waiting_time of the attraction.

        TODO
        Every step that a customer is in an attraction (for a period of attraction_duration),
        waitingtime has to decrease by 1.
        '''

        # PSEUDOCODE:
        # Elke stap dat een customer aan het wachten is moet de wachttijd afnemen

        # 1. Check voor elke attractie wat de wachttijd is.
        # 2. Als de wachttijd groter is dan 1, laat de wachttijd elke stap afnemen.

        if self.current_waitingtime % self.attraction_duration == 0:
            waitingtime = (self.N_current_cust * self.attraction_duration)
            self.current_waitingtime = waitingtime
        else:
            self.current_waitingtime += self.attraction_duration

    def customers_inside(self):
        """Determine the amount of customers inside the Attraction agent."""

        # Get all agents at attraction location
        agents = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            radius=0,
            include_center=True
        )

        # Count customer agents
        counter = 0
        for agent in agents:

            if type(agent) != Route and type(agent) != Attraction:
                counter += 1

        return counter


    def run_attraction(self, amount):
        """Customers enter attraction and leave waiting line."""

        self.cust_in_attr = amount
        self.cust_in_line -= amount

    def step(self):
        """step"""

        # print(self.ride_time)
        # self.calculate_waiting_time()
        self.model.attraction_history[self][self.model.totalTOTAL] = self.N_current_cust
        if self.current_waitingtime > 0:
            self.current_waitingtime -= 1

        if self.N_current_cust > 0:
            self.in_attraction_list.append(1)
        else:
            self.in_attraction_list.append(0)
