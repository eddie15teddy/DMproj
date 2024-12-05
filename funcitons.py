import matplotlib.pyplot as plt
import pandas as pd
import math
from points import Points
import copy
from constants import *
import random


def generate_scatter_plot(points: Points, plot_name = 'plot'):        
    plt.clf()
    
    all_points = points.get_all_points()

    plt.title(plot_name)
    plt.xlabel(X_ROW_NAME)
    plt.ylabel(Y_ROW_NAME)
    plt.scatter(all_points.x, all_points.y, c=all_points.groups, s=all_points.sizes, alpha=all_points.alpha)

def show_scatter_plot(points: Points, plot_name = 'plot', block=True):
    generate_scatter_plot(points, plot_name)
    plt.show(block=block)
    plt.pause(PAUSE_TIME)

def save_scatter_plot(points: Points, plot_name = 'plot'):
    generate_scatter_plot(points, plot_name)
    plt.savefig(f'{plot_name}.png')    

def calculate_distance(point: tuple[float, float], centroid: tuple[float, float]) -> float:
    distance = math.sqrt((centroid[X] - point[X]) ** 2 + (centroid[Y] - point[Y]) ** 2)
    return distance

def get_points_from_file() -> list[(float, float)]:
    print(f"Loading points from {INPUT_FILE_NAME}")

    df = pd.read_csv(INPUT_FILE_NAME)

    points = [(row[X_ROW_NAME], row[Y_ROW_NAME]) for _, row in df.iterrows()]
    return points

def get_cluster_means(points: list[(float, float)], point_groups: list[str], cluster_groups: list[str], centroids: list[(float, float)]) -> dict[str, float]:
    amount_dict = {group: (0, 0) for group in cluster_groups}
    count_dict = {group: 0 for group in cluster_groups}
    means = {group: 0 for group in cluster_groups}

    for i, cur_group in enumerate(point_groups):
        curX, curY = amount_dict[cur_group]
        newX = curX + points[i][X]
        newY = curY + points[i][Y]
        amount_dict[cur_group] = (newX, newY)
        
        count_dict[cur_group] = count_dict[cur_group] + 1
    
    j = 0
    for key, value in amount_dict.items():

        if count_dict[key] == 0:
            mean_x = centroids[j][X]
            mean_y = centroids[j][Y]
        else:
            mean_x = value[X]/ count_dict[key]
            mean_y = value[Y] / count_dict[key]
        means[key] = (mean_x, mean_y)

        j = j +1
    return means

def run_clustering_from_file(plot_name: str, starting_centroids: list[float, float], colours_groups: list[str], 
                             show: bool = False, save: bool = False) -> Points:
    points = Points(get_points_from_file(), centroids=starting_centroids)
    
    return run_clustering_from_points(plot_name, colours_groups, 
                                      points, show, save)

def run_clustering_from_points(plot_name: str, colours_groups: list[str], points: Points, show: bool = False, save: bool = False) -> Points:  
    old_means = None
    means = copy.deepcopy(points.centroids.points)
    points_clustered = copy.deepcopy(points)

    points_clustered.assign_points_to_cluster()

    if show:
        show_scatter_plot(points_clustered, f"{plot_name}-0", False)
    if save:
        save_scatter_plot(points_clustered, f"{plot_name}-0")

    i = 0
    while not old_means == means:
        i = i + 1

        old_means = means

        points_clustered.assign_points_to_cluster()

        means = list(get_cluster_means(points_clustered.points, points_clustered.groups, colours_groups, means).values())
        points_clustered.centroids = Points.create_centroids(means)


        if show:
            show_scatter_plot(points_clustered, f"{plot_name}-{i}", False)
        if save:
            save_scatter_plot(points_clustered, f"{plot_name}-{i}")

    return points_clustered

# Adds number_of_points to points. passed object is modified
def add_random_points(number_of_points: int, points: Points,
                      save: bool = False, show: bool = False, plot_name: str = 'plot', reclustering: bool = True):

    for i in range(number_of_points):
        cur_plot_name = f'{plot_name}-{i}'
        # generate new point
        if show:
            print(f"Generating point {i}")
        new_point = (random.randint(MIN_AGE, MAX_AGE), random.randint(MIN_SCORE, MAX_SCORE))

        # add new point to graph
        if show or save:
            points.append(new_point, group='yellow', size=1000, alpha=.5)
            points.append(new_point, group='black')
            if show:
                show_scatter_plot(points, block=False, plot_name=cur_plot_name)
            if save:
                save_scatter_plot(points, plot_name=cur_plot_name)

            points.remove_last()
            points.remove_last()

        # assign point to a new cluster
        closest_centroid_index = min(
                enumerate(points.centroids.points),
                key = lambda x: calculate_distance(new_point, x[1])
            )[0]

        new_point_cluster = COLOURS[closest_centroid_index]
        
        points.append(new_point, new_point_cluster)
        if show:
            show_scatter_plot(points, block=False, plot_name=cur_plot_name)
        if save:
            save_scatter_plot(points, plot_name=cur_plot_name)

            
        # move centroid
        cluster_size = points.get_group_size(new_point_cluster)
        centroid_index = COLOURS.index(new_point_cluster)
        new_centroid_x = (cluster_size * points.centroids.points[centroid_index][X] + new_point[X]) / (cluster_size + 1)
        new_centroid_y = (cluster_size * points.centroids.points[centroid_index][Y] + new_point[Y]) / (cluster_size + 1)
        points.centroids.points[centroid_index] = (new_centroid_x, new_centroid_y)

        if show:
            show_scatter_plot(points, block=False, plot_name=cur_plot_name)
        if save:
            points.append(new_point, group='yellow', size=1000, alpha=.5)
            save_scatter_plot(points, plot_name=cur_plot_name)
            points.remove_last()

        if reclustering:
            group_spread = points.original_cluster_spread
            total_move_ratio = 0
            for j, colour in enumerate(COLOURS):
                cur_cent = points.centroids.points[j]
                cur_cent_og = points.original_centroids.points[j]

                dist_cur_cent_moved = calculate_distance(cur_cent, cur_cent_og)
                total_move_ratio += dist_cur_cent_moved / group_spread[colour]
            
            print(f"Total move ratio: {total_move_ratio}")
            if total_move_ratio >= RECLUSTERING_THRESHOLD:
                print("Time to recluster")
                points.centroids = Points.create_centroids(CENTROIDS)
                points = run_clustering_from_points(f"{cur_plot_name} - R", COLOURS, points, show=show, save=save)
                points.update_original_cluster_spread()
                points.update_original_centroids()
    
    return points
