from graph import Graph

def get_graph(file_name: str) -> Graph:
    graph = Graph()
    with open(file_name, "r") as file:
        for line in file:
            nodes = line.strip().split(" ")
            graph.add_edge(nodes[0], nodes[1])
    return graph


def get_top_nodes_by_degree(graph: Graph,num:int) -> list[str]:
    return sorted(graph.get_nodes(), key=lambda x: graph.get_neighbors_count(x), reverse=True)[:num]

def get_top_nodes_by_vote(graph: Graph,num:int) -> list[str]:
    res = []
    
    #init the vote ability of each node
    vote_ability = {}
    for node in graph.get_nodes():
        # the vote ability of each node is 1
        vote_ability[node] = 1
    
    # select the top nodes with the highest vote ability
    for i in range(num):
        # if there are no nodes left, break
        if len(vote_ability) == 0:
            break
        max_vote = 0
        max_node = None
        node_vote_record = {}
        for (node, vote) in vote_ability.items():
            for neighbor in graph.get_neighbors(node):
                if neighbor in node_vote_record:
                    node_vote_record[neighbor] += vote
                    
        for (node,score) in node_vote_record.items():
            if score > max_vote:
                max_vote = score
                max_node = node
        print(i,'find max node:', max_node)
        res.append(max_node)
        # TODO select the k
        
        
        # supress the vote ability of the selected node and its neighbors (to ring 3 as simpilfied)
        for neighbor in graph.get_neighbors(max_node):
            for grand_neighbor in graph.get_neighbors(neighbor):
                if grand_neighbor in vote_ability:
                    vote_ability[grand_neighbor] -= 
        
        
if __name__ == "__main__":
    graph = get_graph("12831.edges")

    top10_nodes_by_degree = get_top_nodes_by_degree(graph,10)
    top10_nodes_by_vote = get_top_nodes_by_vote(graph,10)

    infected_nodes_by_degree = sir_simulation(
        graph, top10_nodes_by_degree, beta=0.1)
    infected_nodes_by_vote = sir_simulation(
        graph, top10_nodes_by_vote, beta=0.1)

    print("by degree: ", infected_nodes_by_degree)
    print("by vote: ", infected_nodes_by_vote)