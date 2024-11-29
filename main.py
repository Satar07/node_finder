
if __name__ == "__main__":
    graph = get_graph("12831.edges")
    
    top10_nodes_by_degree = get_top10_nodes_by_degree(graph)
    top10_nodes_by_vote = get_top10_nodes_by_vote(graph)
    
    infected_nodes_by_degree = sir_simulation(graph, top10_nodes_by_degree, beta = 0.1)
    infected_nodes_by_vote = sir_simulation(graph, top10_nodes_by_vote, beta = 0.1)
    
    
    print("by degree: ", infected_nodes_by_degree)
    print("by vote: ", infected_nodes_by_vote)
    
def get_graph(file_name:str) -> Graph:
    graph = Graph()
    with open(file_name, "r") as file:
        for line in file:
            nodes = line.strip().split(" ")
            graph.add_edge(nodes[0], nodes[1])
    return graph

class Graph:
    def __init__(self):
        self.edges = {}
        
    def add_edge(self, node1, node2):
        if node1 not in self.edges:
            self.edges[node1] = []
        if node2 not in self.edges:
            self.edges[node2] = []
        self.edges[node1].append(node2)
        self.edges[node2].append(node1)
        
    def get_neighbors(self, node):
        return self.edges[node]
    
    def get_nodes(self):
        return self.edges.keys()
    
    def get_edges(self):
        return self.edges