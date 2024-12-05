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
points_rerun = run_clustering_from_points('regular', COLOURS, points_add_copy, show=False)

save_scatter_plot(points_rerun, plot_name='regular')

# calculate spread in dynamic
group_spead_dynamic, group_count_dynamic = points_add.get_cluster_spread(COLOURS)

print("\nSpread of Dynamic:")
print(group_spead_dynamic)
print(group_count_dynamic)

# calculate spread in regular
group_spread_regular, group_count_regulat = points_rerun.get_cluster_spread(COLOURS)

print(f'\nSpread of Regular:')
print(group_spread_regular)
print(group_count_regulat)
print("end")
