import copy
from constants import *
from typing import Union
import math

class Points:
    def __init__(self, points: list[(float, float)] = [], 
                 groups: list[str] = None, 
                 distances: list[float] = None, 
                 alpha: list[float] = None,
                 sizes: list[float] = None, 
                 centroids: Union['Points', list[(float, float)]] = None, 
                 other_points: Union['Points', list[(float, float)]] = None):
        # set points
        self.points = copy.deepcopy(points)
        self.x = [point[X] for point in points]
        self.y = [point[Y] for point in points]

        self.count = len(points)

        # centroids, original_centroids and other_points are drawn, but removed from the calculations
        if type(centroids) == list: 
            self.centroids = Points.create_centroids(centroids)
        else:
            self.centroids = copy.deepcopy(centroids)
        self.other_points = copy.deepcopy(other_points)

        # orginal_centroids are stored seperately to calculate how much the centroid has moved
        if self.centroids is not None:
            self.update_original_centroids()

        self.alpha = ([1] * self.count if alpha is None else alpha)
        self.groups = ([DK_CENTROID_COLOUR] * self.count if groups is None else groups)
        self.sizes = ([DEF_POINT_SIZE] * self.count if sizes is None else sizes)
        self.distances = ([0] * self.count if distances is None else distances)

    def append(self, point: tuple[float, float], group: str, size: float = DEF_POINT_SIZE, distance: float = None, alpha: float = 1):
        # add point
        self.points.append(point)
        self.x.append(point[X])
        self.y.append(point[Y])

        self.alpha.append(alpha)
        self.groups.append(group)
        self.sizes.append(size)
        self.distances.append(distance)

        self.count += 1

    def remove_last(self):
        self.points.pop()
        self.x.pop()
        self.y.pop()

        self.alpha.pop()
        self.groups.pop()
        self.sizes.pop()
        self.distances.pop()

        self.count -= 1

    def get_group_size(self, group_name: str) -> int:
        return sum(1 for group in self.groups if group == group_name)
    
    def remove_group(self, group_name: str):
        indeces_to_remove = [i for i, group in enumerate(self.groups) if group == group_name]
        
        for index in reversed(indeces_to_remove):
            self.points.pop(index)
            self.x.pop(index)
            self.y.pop(index)
            self.alpha.pop(index)
            self.sizes.pop(index)
            self.distances.pop(index) 
            self.groups.pop(index)

        self.count -= len(indeces_to_remove)  

    def get_group_points(self, group_name: str) -> list[(float, float)]:
        group = [point for point, group in zip(self.points, self.groups) if group == group_name]
        return group
    
    def get_all_points(self):
        # Add points + other_points + original_centroids + centroids

        new_points_list = copy.deepcopy(self.points)                                                        # points
        new_points_list += (self.other_points.points if self.other_points is not None else [])              # other_points
        new_points_list += (self.original_centroids.points if self.original_centroids is not None else [])  # original_centroids
        new_points_list += (self.centroids.points if self.centroids is not None else [])                    # centroids

        new_alpha = copy.deepcopy(self.alpha)                                                               # points
        new_alpha += (self.other_points.alpha if self.other_points is not None else [])                     # other_points
        new_alpha += (self.original_centroids.alpha if self.original_centroids is not None else [])         # original_centroids
        new_alpha += (self.centroids.alpha if self.centroids is not None else [])                           # centroids
        
        new_groups = copy.deepcopy(self.groups)                                                             # points
        new_groups += (self.other_points.groups if self.other_points is not None else [])                   # other_points 
        new_groups += (self.original_centroids.groups if self.original_centroids is not None else [])       # original_centroids
        new_groups += (self.centroids.groups if self.centroids is not None else [])                         # centroids


        new_sizes = copy.deepcopy(self.sizes)                                                               # points
        new_sizes += (self.other_points.sizes if self.other_points is not None else [])                     # other_points
        new_sizes += (self.original_centroids.sizes if self.original_centroids is not None else [])         # original_centroids
        new_sizes += (self.centroids.sizes if self.centroids is not None else [])                           # centroids

        new_points = Points(new_points_list, new_groups, alpha=new_alpha, sizes=new_sizes)

        return new_points

    def create_centroids(centroids: list[float, float]) -> 'Points':
        cent_len = len(centroids)
        points = Points(centroids, groups=[DK_CENTROID_COLOUR] * cent_len, sizes = [DEF_CENTROID_SIZE] * cent_len)
        return points

    def get_cluster_spread(self, groups: list[str]):
        # calculate spread in added
        group_spread = {colour: 0 for colour in groups}
        group_count = {colour: 0 for colour in groups}
        total_distance = 0

        for i, colour in enumerate(groups):
            cur_group = self.get_group_points(colour)
            group_distance = sum(Points._calculate_distance(cur_point, self.centroids.points[i]) for cur_point in cur_group )
            group_spread[colour] = group_distance / len(cur_group)
            group_count[colour] = len(cur_group)
        
            total_distance += group_distance
        
        total_spread = total_distance / self.count

        group_spread['total'] = total_spread
        group_count['total'] = self.count

        return (group_spread, group_count)

    # If centroids is passed, set original_centroids to that. Otherwise set then to current centroids
    def update_original_centroids(self, centroids: 'Points' = None):
        if centroids is None:
            centroids = self.centroids

        self.original_centroids = copy.deepcopy(centroids)
        self.original_centroids.groups = [LT_CENTROID_COLOUR] * centroids.count
        self.original_centroids.alpha = [0.5] * centroids.count
    
    def _calculate_distance(point: tuple[float, float], centroid: tuple[float, float]) -> float:
        distance = math.sqrt((centroid[X] - point[X]) ** 2 + (centroid[Y] - point[Y]) ** 2)
        return distance