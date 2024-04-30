from helpers import compress, search, get_dicts


class MapAlgorithm:
    def __init__(self):
        self.map = None
        self.compressed_x = None
        self.compressed_y = None

    def preparation(self, rectangles):
        if rectangles:
            self.compressed_x, self.compressed_y = compress(rectangles)
            compressed_dict_x, compressed_dict_y = get_dicts(self.compressed_x, self.compressed_y)
            self.map = [[0] * len(self.compressed_y) for _ in range(len(self.compressed_x))]
            for r in rectangles:
                for x in range(compressed_dict_x[r.x1], compressed_dict_x[r.x2]):
                    for y in range(compressed_dict_y[r.y1], compressed_dict_y[r.y2]):
                        self.map[x][y] += 1

    def query(self, x, y):
        if self.compressed_x:
            x = search(x, self.compressed_x)
            y = search(y, self.compressed_y)
            if x == -1 or y == -1:
                return 0
            else:
                return self.map[x][y]
        else:
            return 0
