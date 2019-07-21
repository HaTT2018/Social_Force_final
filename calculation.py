import numpy as np
import math
import operation

def calculate_center_of_destination(img,l):
    #find the center(actually it's an area) of the entrance area, this step looks useless
    rw = np.where(img>70)[0]
    cw = np.where(img>70)[1]
    c_rw = [i+int(rw.mean()*np.ones(l)[i])-int(l/2) for i in range(np.size(rw.mean()*np.ones(l)))] #center coordinate of white area
    c_cw = [i+int(cw.mean()*np.ones(l)[i])-int(l/2) for i in range(np.size(cw.mean()*np.ones(l)))]

    (c_rw,c_cw) = np.meshgrid(c_rw,c_cw)
    img[c_rw,c_cw]=100
    return img, c_rw, c_cw

def calculate_direction_vector(population_shape, population_coordinate_set, destination):
    direction_vector_set = np.dot(np.ones((population_shape[0],1)),destination) - population_coordinate_set
    direction_vector_set = np.array([i/np.linalg.norm(i) for i in direction_vector_set])
    return direction_vector_set

def calculate_initial_velocity(mean, std, population_shape):
    initail_speed_set = np.random.normal(mean, std, (population_shape[0],1))
    angel = 0#rad
    angle_std = 0.5#rad
    angel_set = np.random.normal(angel, angle_std, population_shape[0])
    direction_set = np.array([[math.cos(i) for i in angel_set],[math.sin(i) for i in angel_set]]).T
    initial_velocity_set = initail_speed_set * direction_set
    return initial_velocity_set, initail_speed_set

def calculate_driven_force(population_mass_set, max_speed_set, direction_vector_set, velocity_set, reaction_time):
    driven_acceleration_set = 1/reaction_time * (max_speed_set * direction_vector_set - velocity_set)
    driven_force_set = driven_acceleration_set * population_mass_set
    return driven_force_set

def calculate_population_repulsion(population_coordinate_set, velocity_set, view_distance, view_angel, dt):
    velocity_unit_direction_vector_set = np.array([i/np.linalg.norm(i) for i in velocity_set])
    #view field is 10 meters aways from each person and 200 degrees of view width
    population_repulsion_set = []
    for i in range(np.shape(population_coordinate_set)[0]):
        population_relative_coordinate_set = population_coordinate_set - population_coordinate_set[i]
        population_relative_distance_set = np.array([[np.linalg.norm(i)] for i in population_relative_coordinate_set])
        population_normal_vector = population_relative_coordinate_set/population_relative_distance_set
        population_observed = np.array([(0, 0, 0)])
        
        for j in range(np.shape(population_coordinate_set)[0]):
            if np.degrees(np.arccos(np.dot(population_normal_vector[j], velocity_unit_direction_vector_set[i]))) \
                <= view_angel/2 and population_relative_distance_set[j] <= view_distance:
                population_observed = np.vstack((population_observed, np.hstack((population_coordinate_set[j], j)) ))#i, j are the indexes where the person is
            
        population_observed = np.delete(population_observed, [0], axis=0)
        r = [int(ii) for ii in population_observed[:,2]]

        b_set = 0.5 * np.sqrt((population_relative_distance_set[r] + population_relative_distance_set[r]-velocity_set[r]*dt)**2 - (velocity_set[r]*dt)**2)

        repulsion_i = -2.1 * np.exp(-b_set/0.3) * population_normal_vector[r]

        population_repulsion_set.append(repulsion_i)

    population_repulsion_set = np.array(population_repulsion_set).T
    resultant_population_repulsion_set = np.array([np.mean(iii, axis=0) for iii in population_repulsion_set])
    resultant_population_repulsion_set[np.isnan(resultant_population_repulsion_set)]=0
    return resultant_population_repulsion_set

def calculate_obstacle_repulsion():
    return
