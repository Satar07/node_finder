class Graph:
    def __init__(self):
        self.edges = {}

    def add_edge(self, node1: int, node2: int):
        if node1 not in self.edges:
            self.edges[node1] = []
        if node2 not in self.edges:
            self.edges[node2] = []
        self.edges[node1].append(node2)

    def get_neighbors(self, node) -> list[int]:
        return self.edges[node]

    def get_nodes(self) -> list[int]:
        return self.edges.keys()

    def get_edges(self) -> dict[int, list[int]]:
        return self.edges

    def get_neighbors_count(self, node) -> int:
        return len(self.edges[node])