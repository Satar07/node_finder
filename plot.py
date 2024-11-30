import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 读取JSON文件
with open('simulation_results.json') as f:
    data = json.load(f)

# 提取数据
top_nodenum = []
beta = []
diff = []

for entry in data:
    top_nodenum.append(entry['top_nodenum'])
    beta.append(entry['beta'])
    diff.append(-entry['infected_nodes_by_degree'] +
                entry['infected_nodes_by_vote'])

# 创建三维图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制散点图
ax.scatter(top_nodenum, beta, diff, c='r', marker='o')

# 设置坐标轴标签
ax.set_xlabel('Top Node Number')
ax.set_ylabel('Beta')
ax.set_zlabel('Difference (Vote-Degree)')

# 显示图形
plt.show()
