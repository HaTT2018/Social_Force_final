import numpy as np

def if_overspeed(max_speed_set, velocity_set):
    speed_set = np.array([[np.linalg.norm(i)] for i in velocity_set])
    direction_set = velocity_set / speed_set
    overspeed_index = np.array(np.where(speed_set >= max_speed_set))[0,:]
    velocity_set[overspeed_index] = max_speed_set[overspeed_index] * direction_set[overspeed_index]
    return velocity_set

def if_finished(population_coordinate_set):
    return np.size(population_coordinate_set) == 0

