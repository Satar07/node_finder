import json
import matplotlib.pyplot as plt

# Load the data from the JSON file
with open("simulation_results.json", "r") as file:
    data = json.load(file)

# Extract the relevant data
top_nodenum_values = sorted(set(item["top_nodenum"] for item in data))
beta_values = sorted(set(item["beta"] for item in data))

# Prepare data for plotting
degree_results = {beta: [] for beta in beta_values}
vote_results = {beta: [] for beta in beta_values}

for beta in beta_values:
    for top_nodenum in top_nodenum_values:
        for item in data:
            if item["beta"] == beta and item["top_nodenum"] == top_nodenum:
                degree_results[beta].append(item["infected_nodes_by_degree"])
                vote_results[beta].append(item["infected_nodes_by_vote"])

# Plot the data
plt.figure(figsize=(12, 8))

for beta in beta_values:
    plt.plot(top_nodenum_values, degree_results[beta], label=f'Degree (beta={beta})', marker='o')
    plt.plot(top_nodenum_values, vote_results[beta], label=f'Vote (beta={beta})', marker='x')

plt.xlabel('Top Node Num')
plt.ylabel('Infected Nodes')
plt.title('Infected Nodes by Top Node Num and Beta')
plt.legend()
plt.grid(True)
plt.show()