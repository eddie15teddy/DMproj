from funcitons import calculate_distance, run_clustering_from_file, show_scatter_plot, save_scatter_plot, run_clustering_from_points, add_random_points;
from constants import *
from points import Points
import time
import copy


time.sleep(5)
# cluster from file
points = run_clustering_from_file(PLOT_NAME, CENTROIDS, COLOURS)

# add original centroids and 100 random points
other_points = Points()
for centroid in points.centroids.points:
    other_points.append(centroid, LT_CENTROID_COLOUR, DEF_CENTROID_SIZE, alpha=0.5)
points.other_points = other_points
points_add = add_random_points(NEW_POINTS, points, False, show = False)

save_scatter_plot(points_add, plot_name='dynamic')

# recluster the new points
points_add_copy = copy.deepcopy(points_add)
points_add_copy.centroids = Points(CENTROIDS)
points_add_copy.other_points = None
points_rerun = run_clustering_from_points('regular', COLOURS, points_add_copy, show=True)

save_scatter_plot(points_rerun, plot_name='regular')

# calculate spread in added
group_spread_added = {colour: 0 for _, colour in enumerate(COLOURS)}
group_count_added = {colour: 0 for _, colour in enumerate(COLOURS)}
total_distance_added = 0
for i, colour in enumerate(COLOURS):
    cur_group = points_add.get_group_points(colour)
    group_distance = sum(calculate_distance(cur_point, points_add.centroids.points[i]) for cur_point in cur_group )
    group_spread_added[colour] = group_distance / len(cur_group)
    group_count_added[colour] = len(cur_group)

    total_distance_added += group_distance

total_spread_added = total_distance_added / points_add.count

print(f'\nSpread of Added: {total_spread_added}')
print(group_spread_added)
print(group_count_added)

# calculate spread in rerun
group_spread_rerun = {colour: 0 for _, colour in enumerate(COLOURS)}
group_count_rerun = {colour: 0 for _, colour in enumerate(COLOURS)}
total_distance_rerun = 0
for i, colour in enumerate(COLOURS):
    cur_group = points_rerun.get_group_points(colour)
    group_distance = sum(calculate_distance(cur_point, points_rerun.centroids.points[i]) for cur_point in cur_group )
    group_spread_rerun[colour] = group_distance / len(cur_group)
    group_count_rerun[colour] = len(cur_group)

    total_distance_rerun += group_distance

total_spread_rerun = total_distance_rerun / points_rerun.count

print(f'\nSpread of Rerun: {total_spread_rerun}')
print(group_spread_rerun)
print(group_count_rerun)
print("end")



#