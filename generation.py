import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time


def generate_standardized_map(path):
    #Read map
    img = mpimg.imread(path)
    img = img.mean(axis=2)
    img[np.where(img>70)] = 255
    img[np.where(img<=70)] = 0
    return img

def generate_person(born_points, max_population_one_time):
    #born_points is a list or array contains
    #all the born points of one born place
    
    #population generated should be less than some value
    population = np.random.randint(1,max_population_one_time)
    
    #each person has his/her mass
    sign = np.floor(np.random.random(population) - 0.5)
    sign[np.where(sign==0)]=1
    population_mass_set = sign * np.random.random(population) * 10 + 60
    population_mass_set = np.reshape(population_mass_set, (population,1))

    #each person has his/her born coordinate
    born_cdnt = np.array([born_points[np.random.randint(np.size(born_points)/2)] for i in range(population)], dtype=float)# a random chosen born point coordinate
    
    return population_mass_set, born_cdnt
    
def generate_potential_field(img,c_rw,c_cw):
#image, row coordinate of the center of white area, column coordinate of the center of white area, 
#generate the potential field, an old algorithm, also useless in social force modeling
    t_r = np.arange(np.shape(img)[0]) - c_rw
    t_c = np.arange(np.shape(img)[1]) - c_cw

    (t_r,t_c) = np.meshgrid(t_r,t_c)
    distance_field = ((np.array([i**2 for i in t_r]) + np.array([i**2 for i in t_c]))**0.5)

    fig = plt.figure(figsize=[12, 6], dpi=150)
    f1 = fig.add_subplot(121)
    r1 = f1.imshow(distance_field.T)#this transpose only fot visulization(result1)
    f1.plot(c_cw,c_rw,'r*')#this transpose only fot visulization
    plt.colorbar(r1)

    f2 = fig.add_subplot(122,projection = '3d')
    f2.set_aspect('equal')
    r2 = f2.plot_surface(t_r,t_c,distance_field,cmap='rainbow')
    plt.colorbar(r2)
    plt.xlim([0, 400])
    plt.show()
    

def generate_population_plot(population_coordinate_set, img, iteration_time, root_path):
    plt.figure(figsize=[10, 10], dpi=150)
    plt.ion()

    plt.cla()
    plt.imshow(img)
    r = population_coordinate_set[:,0]
    c = population_coordinate_set[:,1]
    plt.plot(c,r,'r.', ms=.2)
    plt.xlim([0, 400])
    plt.pause(.001)

    plt.ioff()
    plt.savefig(root_path + r'pics\\%i.jpg'%iteration_time)

def generate_resultant_force_set(driven_force_set, population_repulsion_set):
    return driven_force_set + population_repulsion_set