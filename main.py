import json
import random
from graph import Graph
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed


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


vote_result = []


def get_top_nodes_by_vote(graph: Graph, num: int = 100) -> list[str]:
    global vote_result
    if len(vote_result) < num:
        vote_result.clear()
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

        vote_result = res
    return vote_result[:num]


def sir_simulation(graph: Graph, infected_nodes: list[str], beta: float, gamma: float = 0.5) -> int:
    process_bar = tqdm(desc="SIR Simulation", total=graph.get_nodes_count())

    # init the set of susceptible nodes, infected nodes and recovered nodes
    susceptible_nodes = set(graph.get_nodes())
    infected_nodes = set(infected_nodes)
    recovered_nodes = set()

    # remove the infected nodes from the susceptible nodes
    for node in infected_nodes:
        susceptible_nodes.remove(node)

    # simulation
    flag = True
    while flag:
        flag = False
        new_infected_nodes = set()
        new_recovered_nodes = set()
        for node in infected_nodes:
            # spread the virus
            for neighbor in graph.get_neighbors(node):
                if neighbor in susceptible_nodes and random.uniform(0, 1) < beta:
                    flag = True
                    new_infected_nodes.add(neighbor)
                    susceptible_nodes.remove(neighbor)

            # recover from the virus
            if random.uniform(0, 1) < gamma:
                new_recovered_nodes.add(node)
                flag = True

        # update the status of nodes
        infected_nodes.update(new_infected_nodes)
        infected_nodes.difference_update(new_recovered_nodes)
        recovered_nodes.update(new_recovered_nodes)

        process_bar.update(len(new_infected_nodes))

    process_bar.close()
    return len(recovered_nodes) + len(infected_nodes)


def run_simulation(graph, top_nodes_by_degree, top_nodes_by_vote, beta):
    sum_infe = 0
    sum_vote = 0

    for _ in range(5):
        sum_infe += sir_simulation(graph, top_nodes_by_degree, beta=beta)
        sum_vote += sir_simulation(graph, top_nodes_by_vote, beta=beta)

    return sum_infe / 5, sum_vote / 5


if __name__ == "__main__":
    graph = get_graph("./twitter_combined.txt")
    print("Nodes count: ", graph.get_nodes_count())
    print("Edges count: ", graph.get_egde_count())

    # Define the range of values for top_nodenum and beta
    top_nodenum_values = [1, 3, 5, 10, 20, 40]
    beta_values = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1]

    results = []
    get_top_nodes_by_vote(graph)

    with ThreadPoolExecutor() as executor:
        futures = []
        for top_nodenum in tqdm(top_nodenum_values, desc="Top Node Num Loop"):
            for beta in tqdm(beta_values, desc="Beta Loop", leave=False):
                top_nodes_by_degree = get_top_nodes_by_degree(graph, top_nodenum)
                top_nodes_by_vote = get_top_nodes_by_vote(graph, top_nodenum)
                futures.append(executor.submit(run_simulation, graph, top_nodes_by_degree, top_nodes_by_vote, beta))

        for future in tqdm(as_completed(futures), total=len(futures), desc="Simulation Progress"):
            top_nodenum, beta, (infected_nodes_by_degree, infected_nodes_by_vote) = future.result()
            result = {
                "top_nodenum": top_nodenum,
                "beta": beta,
                "infected_nodes_by_degree": infected_nodes_by_degree,
                "infected_nodes_by_vote": infected_nodes_by_vote
            }
            results.append(result)

    # Save the results to a file
    with open("simulation_results.json", "w") as file:
        json.dump(results, file, indent=4)

    print("Results saved to simulation_results.json")