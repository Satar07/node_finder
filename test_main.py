import unittest
from main import get_top_nodes_by_vote, get_top_nodes_by_degree
from graph import Graph

# FILE: test_main.py


class TestGetTopNodes(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.graph.add_edge(0,1)
        self.graph.add_edge(0,2)
        self.graph.add_edge(0,3)
        self.graph.add_edge(0,4)
        self.graph.add_edge(1,6)
        self.graph.add_edge(2,6)
        self.graph.add_edge(3,6)
        self.graph.add_edge(4,6)
        self.graph.add_edge(0,5)
        self.graph.add_edge(7,8)
        self.graph.add_edge(7,5)
        self.graph.add_edge(7,9)
        
    def test_get_top_nodes_by_vote1(self):
        self.assertEqual(get_top_nodes_by_vote(self.graph, 1), [0])
        
    def test_get_top_nodes_by_vote2(self):
        nodes = get_top_nodes_by_vote(self.graph, 2)
        self.assertIn(0, nodes)
        self.assertIn(7, nodes)
        
    def test_get_top_nodes_by_degree(self):
        self.assertEqual(get_top_nodes_by_degree(self.graph, 2), [0, 6])
        

if __name__ == "__main__":
    unittest.main()