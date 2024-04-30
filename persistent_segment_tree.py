from helpers import Event, Node, compress, search, get_dicts


class PersistentTreeAlgorithm:
    def __init__(self):
        self.compressed_x = None
        self.compressed_y = None
        self.tree = None

    def preparation(self, rectangles):
        if rectangles:
            self.compressed_x, self.compressed_y, = compress(rectangles)
            compressed_dict_x, compressed_dict_y = get_dicts(self.compressed_x, self.compressed_y)
            event_list = []
            for r in rectangles:
                event_list.append(Event(compressed_dict_x[r.x1], compressed_dict_y[r.y1], compressed_dict_y[r.y2], 1))
                event_list.append(Event(compressed_dict_x[r.x2], compressed_dict_y[r.y1], compressed_dict_y[r.y2], -1))
            self.tree = PersistentSegmentTree(sorted(event_list, key=lambda e: e.val), len(self.compressed_y))

    def query(self, x, y):
        if self.compressed_x:
            x = search(x, self.compressed_x)
            y = search(y, self.compressed_y)
            if x == -1 or y == -1 or len(self.tree.nodes) <= x:
                return 0
            else:
                return self.tree.find(x, y)
        else:
            return 0


class PersistentSegmentTree:
    def __init__(self, event_list, size):
        self.nodes = []
        self.root = self.build_tree(0, size)
        val = event_list[0].val
        for event in event_list:
            if event.val != val:
                self.nodes.append(self.root)
                val = event.val
            self.root = self.append(self.root, event.start, event.end, event.is_end)

    def build_tree(self, left, right):
        if right - 1 == left:
            return Node(None, None, left, right, 0)
        middle = (left + right) // 2
        left = self.build_tree(left, middle)
        right = self.build_tree(middle, right)
        return Node(left, right, left.left, right.right, left.total + right.total)

    def append(self, node, left, right, val):
        if left <= node.left and right >= node.right:
            return Node(node.left_node, node.right_node, node.left, node.right, node.total + val)
        if node.left >= right or node.right <= left:
            return node
        root = Node(node.left_node, node.right_node, node.left, node.right, node.total)
        root.left_node = self.append(root.left_node, left, right, val)
        root.right_node = self.append(root.right_node, left, right, val)
        return root

    def find(self, x, q):
        return self.search(self.nodes[x], q)

    def search(self, node, q):
        if node is None:
            return 0
        m = (node.left + node.right) // 2
        if q < m:
            return node.total + self.search(node.left_node, q)
        else:
            return node.total + self.search(node.right_node, q)
