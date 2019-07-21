import generation
import calculation
import operation
import numpy as np
import judge
import time



start_time = time.time()
root_path = '/Users/harrisonzhang/Desktop/Social_Force-master/'
imgname = 's.jpg'

img = generation.generate_standardized_map(root_path+imgname)

#since the function is useless, I don't involk it
#[img, c_rw, c_cw] = calculate_center_of_destination(img,l=1)
c_rw, c_cw = 425, 209

#destination coordinate
destination = np.array([[c_rw, c_cw]])

#generate_potential_field(img,c_rw,c_cw)

#initialize the born points, a small square located at the left top
x = [int(i+100 + np.zeros(10)[i]) for i in range(10)]
y = [int(i+100 + np.zeros(10)[i]) for i in range(10)]
x, y = np.meshgrid(x,y)
born_points = [(x.reshape(1,100)[0,i], y.reshape(1,100)[0,i]) for i in range(np.size(x))]


std = 0.26#m/s
mean = 1.34#m/s
speed_ratio = 1.3
reaction_time = 0.2#second
view_distance = 10#meter
view_angel = 200#degree
dt = 10 #time duration between each iteration


#initialize the max_population_one_time, depending on the population flow speed
max_population_one_time = 10
#obtain the properties of people which is newly generated
[new_population_mass_set, born_cdnt] = generation.generate_person(born_points, max_population_one_time)

#obtain newly generated persons' initial speeds, which is stochastic 
initial_velocity_set, initial_speed_set = calculation.calculate_initial_velocity(mean, std, np.shape(born_cdnt))

#add people into population_coordinate_set
population_coordinate_set = born_cdnt
population_mass_set = new_population_mass_set
population_shape = np.shape(population_coordinate_set)

#obtain each person's direction_vector e, which points from each person to the destination
direction_vector_set = calculation.calculate_direction_vector(population_shape, population_coordinate_set, destination)

#calculate the maximum speed of each person
max_speed_set = initial_speed_set * speed_ratio

#add newly generated people into the population_coordinate_set
velocity_set = initial_velocity_set

#walk
population_coordinate_set = operation.walk(population_coordinate_set, velocity_set, dt)
generation.generate_population_plot(population_coordinate_set, img, 00)

#calculate_driven_force
driven_force_set = calculation.calculate_driven_force(population_mass_set, max_speed_set, direction_vector_set, velocity_set, reaction_time)

#calculate_population_repulsion
population_repulsion_set = calculation.calculate_population_repulsion(population_coordinate_set, velocity_set, view_distance, view_angel, dt)

#calculate_obstacle_repulsion

#generate_resultant_force_set
resultant_force_set = generation.generate_resultant_force_set(driven_force_set, population_repulsion_set)

#update velocity
velocity_set = operation.update_velocity(resultant_force_set, velocity_set, population_mass_set, dt)

#judge if the speed is overspeed, if true, set the speed to max speed
velocity_set = judge.if_overspeed(max_speed_set, velocity_set)


for iteration_time in range(1000):
    looptime_s = time.time()
    #obtain the properties of people which is newly generated
    [new_population_mass_set, born_cdnt] = generation.generate_person(born_points, max_population_one_time)

    #obtain newly generated persons' initial speeds, which is stochastic 
    initial_velocity_set, initial_speed_set = calculation.calculate_initial_velocity(mean, std, np.shape(born_cdnt))

    population_coordinate_set = np.vstack((population_coordinate_set, born_cdnt))
    population_mass_set = np.vstack((population_mass_set, new_population_mass_set))
    population_shape = np.shape(population_coordinate_set)

    direction_vector_set = calculation.calculate_direction_vector(population_shape, population_coordinate_set, destination)

    max_speed_set = np.vstack((max_speed_set, initial_speed_set * speed_ratio))

    velocity_set = np.vstack((velocity_set, initial_velocity_set))

    #walk
    population_coordinate_set = operation.walk(population_coordinate_set, velocity_set, dt)
    if iteration_time%10==0:
        generation.generate_population_plot(population_coordinate_set, img, iteration_time)



    #judge whether all the people reached the destination
    if judge.if_finished == 1:
        break

    #calculate_driven_force
    driven_force_set = calculation.calculate_driven_force(population_mass_set, max_speed_set, direction_vector_set, velocity_set, reaction_time)

    #calculate_population_repulsion
    population_repulsion_set = calculation.calculate_population_repulsion(population_coordinate_set, velocity_set, view_distance, view_angel, dt)

    #calculate_obstacle_repulsion

    #generate_resultant_force_set
    resultant_force_set = generation.generate_resultant_force_set(driven_force_set, population_repulsion_set)

    #update velocity
    velocity_set = operation.update_velocity(resultant_force_set, velocity_set, population_mass_set, dt)

    #judge if the speed is overspeed, if true, set the speed to max speed
    velocity_set = judge.if_overspeed(max_speed_set, velocity_set)


    looptime_e = time.time()
    print('spent %f'%(looptime_e - looptime_s))








print(np.shape(population_coordinate_set))

end_time = time.time()
total_duration = end_time - start_time
print(total_duration)
a=input()








