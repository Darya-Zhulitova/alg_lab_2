from helpers import Rectangle
from map import MapAlgorithm
from brute_force import BruteForceAlgorithm
from persistent_segment_tree import PersistentTreeAlgorithm

rectangles = []
for i in range(int(input())):
    rectangles.append(Rectangle(*map(int, input().split())))
queries = []
for i in range(int(input())):
    queries.append(list(map(int, input().split())))
# task = BruteForceAlgorithm()
# task = MapAlgorithm()
task = PersistentTreeAlgorithm()
task.preparation(rectangles)
for x, y in queries:
    print(task.query(x, y))
