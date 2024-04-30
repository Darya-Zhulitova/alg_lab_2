class BruteForceAlgorithm:
    def __init__(self):
        self.rectangles = None

    def preparation(self, rectangles):
        self.rectangles = rectangles

    def query(self, x, y):
        k = 0
        for r in self.rectangles:
            if r.x1 <= x < r.x2 and r.y1 <= y < r.y2:
                k += 1
        return k
