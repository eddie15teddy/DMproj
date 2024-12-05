X = 0
Y = 1
DEF_CENTROID_SIZE = 20;
DEF_POINT_SIZE = 40;
PAUSE_TIME = 1;

INPUT_FILE_NAME = "Mall_Customers.csv"
X_ROW_NAME = "Age"
Y_ROW_NAME = "Spending Score"
PLOT_NAME = f"{X_ROW_NAME} vs {Y_ROW_NAME}"
DEF_CENTROID_SIZE = 20;

X = 0
Y = 1

# CENTROIDS = [(1, 1), (35, 1), (55, 1), ]
CENTROIDS = [(1, 1), (20, 1), (40, 1), (60, 1)]
# CENTROIDS = [(70, 100), (71, 101), (72, 102), (73, 103)]

COLOURS = ['red', 'green', 'blue', 'orange']
# COLOURS = ['red', 'green', 'blue']

LT_CENTROID_COLOUR = 'grey'
DK_CENTROID_COLOUR = 'black'

NEW_POINTS = 55
MIN_AGE = 45
MAX_AGE = 70
MIN_SCORE = 80
MAX_SCORE = 100

RECLUSTERING_THRESHOLD = .25