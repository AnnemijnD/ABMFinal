from mesa import Agent
import random
import math
import numpy as np

class Monitor(Agent):

    def __init__(self, max_time_steps, num_attractions, attraction_positions):
        self.time_dict = self.make_time_dict(max_time_steps, num_attractions)
        self.attraction_positions = attraction_positions

    def make_time_dict(self, max_time_steps, num_attractions):
        attraction_list = [0] * num_attractions
        dict = {}

        for step in range(max_time_steps):
            dict[step] = attraction_list

        return dict


    def time_dict_increment(self,next_goal, predicted_arrival_time):


        self.time_dict[predicted_arrival_time][next_goal] += 1


    def time_dict_decrement(self, attraction, time):

        self.time_dict[time][attraction] -= 1


    def make_prediction(self, current_step, goals, distances):

        predictions = {}
        arrival_times = {}

        for attraction in goals:
            arrival_time = int(current_step + distances[attraction.unique_id])
            predicted_waiting_time = self.time_dict[arrival_time][attraction.unique_id]
            predictions[attraction] = predicted_waiting_time
            arrival_times[attraction] = arrival_time

        minval = min(predictions.values())
        res = [k for k, v in predictions.items() if v==minval]
        if len(res) is 1:
            predicted_attraction = res[0]
        else:
            predicted_attraction = random.choice(res)

        predicted_arrival_time = arrival_times[predicted_attraction]
        self.time_dict_increment(predicted_attraction.unique_id, predicted_arrival_time)

        return predicted_attraction.pos
