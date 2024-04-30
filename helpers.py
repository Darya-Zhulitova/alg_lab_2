class Event:
    def __init__(self, val, start, end, is_end):
        self.val = val
        self.start = start
        self.end = end
        self.is_end = is_end


class Node:
    def __init__(self, left_node, right_node, left, right, total):
        self.left_node = left_node
        self.right_node = right_node
        self.left = left
        self.right = right
        self.total = total


class Rectangle:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


def compress(rectangles):
    set_x = set()
    set_y = set()
    for r in rectangles:
        set_x.add(r.x1)
        set_y.add(r.y1)
        set_x.add(r.x2)
        set_y.add(r.y2)
    return list(sorted(set_x)), list(sorted(set_y))


def get_dicts(compressed_x, compressed_y):
    compressed_dict_x = dict()
    compressed_dict_y = dict()
    for x in range(len(compressed_x)):
        compressed_dict_x[compressed_x[x]] = x
    for y in range(len(compressed_y)):
        compressed_dict_y[compressed_y[y]] = y
    return compressed_dict_x, compressed_dict_y


def search(query, array):
    low = 0
    high = len(array)
    while low < high:
        mid = low + (high - low) // 2
        if array[mid] <= query:
            low = mid + 1
        else:
            high = mid
    return low - 1
