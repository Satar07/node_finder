import random
from graph import Graph
from tqdm import tqdm


def get_graph(file_name: str) -> Graph:
    graph = Graph()
    with open(file_name, "r") as file:
        for line in file:
            nodes = line.strip().split(" ")
            if len(nodes) != 2:
                continue
            graph.add_edge(nodes[0], nodes[1])
    return graph


def get_top_nodes_by_degree(graph: Graph, num: int) -> list[str]:
    return sorted(graph.get_nodes(), key=lambda x: graph.get_neighbors_count(x), reverse=True)[:num]


def get_top_nodes_by_vote(graph: Graph, num: int) -> list[str]:
    res = []

    # init the vote ability of each node
    vote_ability = {}
    for node in graph.get_nodes():
        # the vote ability of each node is 1
        vote_ability[node] = 1

    # calc the supress factor
    k = 1/graph.get_everage_degree()

    # init the vote score of each node
    vote_score = {}
    for node in graph.get_nodes():
        vote_score[node] = 0
        for neighbor in graph.get_neighbors(node):
            vote_score[node] += vote_ability[neighbor]

    # select the top num nodes, update vote ability and vote score
    for i in tqdm(range(num), desc="Selecting top nodes by vote"):
        if len(vote_score) == 0:
            break
        top_node = max(vote_score, key=vote_score.get)
        res.append(top_node)
        vote_score.pop(top_node)
        vote_ability[top_node] = 0
        for neighbor in graph.get_neighbors(top_node):
            max_supress = max(-vote_ability[neighbor], -k)
            vote_ability[neighbor] += max_supress
            for neighbor_neighbor in graph.get_neighbors(neighbor):
                if neighbor_neighbor in vote_score:
                    vote_score[neighbor_neighbor] += max_supress

    return res


def sir_simulation(graph: Graph, infected_nodes: list[str], beta: float, gamma: float = 0.01) -> int:
    infected = set(infected_nodes)
    infected_next = set(infected_nodes)
    recovered = set()
    progress_bar = tqdm(total=len(graph.get_nodes()), desc="SIR Simulation")
    
    while len(infected) > 0:
        progress_bar.update(1)
        for node in infected:
            for neighbor in graph.get_neighbors(node):
                if neighbor in recovered:
                    continue
                if random.random() < beta:
                    infected_next.add(neighbor)
        for node in infected:
            if random.random() < gamma:
                recovered.add(node)
        infected = infected_next - recovered
        infected_next = set()
    progress_bar.close()
    return len(recovered)


if __name__ == "__main__":
    graph = get_graph("./12831.edges")
    print("Nodes count: ", graph.get_nodes_count())
    print("Edges count: ", graph.get_egde_count())

    top_nodes_by_degree = get_top_nodes_by_degree(graph, 10)
    top_nodes_by_vote = get_top_nodes_by_vote(graph, 10)

    infected_nodes_by_degree = sir_simulation(
        graph, top_nodes_by_degree, beta=0.1)
    infected_nodes_by_vote = sir_simulation(
        graph, top_nodes_by_vote, beta=0.1)

    print("by degree: ", infected_nodes_by_degree)
    print("by vote: ", infected_nodes_by_vote)
