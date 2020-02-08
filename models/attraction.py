from mesa import Agent
import random
try:
    from .route import get_attraction_coordinates, Route
except:
    from route import get_attraction_coordinates, Route

class Attraction(Agent):
    def __init__(self, unique_id, model, pos, name):
        super().__init__(unique_id, model)
        """
        Args:
            id (int): a unique id to represent the agent
            model (Themepark): the model to link the agent to
            pos (tuple(int,int)): the position of the agent (x,y)
            name (str): the name of an attraction
        """

        # agent attributes
        self.name = name
        self.model = model
        self.pos = pos
        self.attraction_duration = 10
        self.current_waitingtime = 0

        # number of customers currently in attraction
        self.N_current_cust = 0

        # number of rides taken in total in this attraction
        self.rides_taken = 0

        # keep up occupation of this attraction
        self.in_attraction_list = []

    def calculate_waiting_time(self):
        '''
        Calculates and updates current waiting_time of the attraction.
        '''

        # calculate waiting time
        if self.current_waitingtime % self.attraction_duration == 0:
            waitingtime = (self.N_current_cust * self.attraction_duration)
            self.current_waitingtime = waitingtime

        # update waiting time
        else:
            self.current_waitingtime += self.attraction_duration

    def step(self):
        '''
        Step
        '''

        # update the attraction waiting time history
        self.model.attraction_history[self][self.model.totalTOTAL] = self.N_current_cust

        # decrease waiting time with one step
        if self.current_waitingtime > 0:
            self.current_waitingtime -= 1

        # keep track of the attraction occupation
        if self.N_current_cust > 0:
            self.in_attraction_list.append(1)
        else:
            self.in_attraction_list.append(0)
