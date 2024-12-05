from funcitons import calculate_distance, run_clustering_from_file, show_scatter_plot, save_scatter_plot, run_clustering_from_points, add_random_points;
from constants import *
from points import Points
import time
import copy


time.sleep(5)
# cluster from file
points = run_clustering_from_file(PLOT_NAME, CENTROIDS, COLOURS)

points_add = copy.deepcopy(points)
points_add.update_original_centroids() 
points_add.update_original_cluster_spread()
# points_add.other_points = Points([(0,0), (100, 0), (0, 100), (100, 100)])
points_add = add_random_points(NEW_POINTS, points_add, show = False, reclustering=True, save=True)

save_scatter_plot(points_add, plot_name='dynamic')

# recluster the new points
points_rerun = copy.deepcopy(points_add)
points_rerun.centroids = Points.create_centroids(CENTROIDS)
points_rerun.update_original_centroids()
points_rerun = run_clustering_from_points('regular', COLOURS, points_rerun, save = True, show=False)
points_rerun.original_centroids = None

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