import numpy

def walk(population_coordinate_set, velocity_set, dt):
    population_coordinate_set += velocity_set * dt
    return population_coordinate_set

def update_velocity(resultant_force_set, velocity_set, population_mass_set, dt):
    acceleration_set = resultant_force_set/population_mass_set
    velocity_set += acceleration_set * dt
    return velocity_set

def get_viewed_population_coordinate_set():
    
    return viewed_population_coordinate_set