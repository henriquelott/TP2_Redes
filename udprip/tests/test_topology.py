import unittest
from src.topology import Topology

class TestTopology(unittest.TestCase):

    def setUp(self):
        self.topology = Topology()

    def test_add_link(self):
        self.topology.add_link("127.0.1.1", "127.0.1.2", 10)
        self.assertIn("127.0.1.2", self.topology.routing_table["127.0.1.1"])
        self.assertEqual(self.topology.routing_table["127.0.1.1"]["127.0.1.2"], 10)

    def test_remove_link(self):
        self.topology.add_link("127.0.1.1", "127.0.1.2", 10)
        self.topology.remove_link("127.0.1.1", "127.0.1.2")
        self.assertNotIn("127.0.1.2", self.topology.routing_table["127.0.1.1"])

    def test_update_routing_table(self):
        self.topology.add_link("127.0.1.1", "127.0.1.2", 10)
        self.topology.add_link("127.0.1.2", "127.0.1.3", 10)
        self.topology.update_routing_table()
        self.assertIn("127.0.1.3", self.topology.routing_table["127.0.1.1"])
        self.assertEqual(self.topology.routing_table["127.0.1.1"]["127.0.1.3"], 20)

    def test_link_failure(self):
        self.topology.add_link("127.0.1.1", "127.0.1.2", 10)
        self.topology.add_link("127.0.1.2", "127.0.1.3", 10)
        self.topology.remove_link("127.0.1.1", "127.0.1.2")
        self.topology.update_routing_table()
        self.assertNotIn("127.0.1.2", self.topology.routing_table["127.0.1.1"])

if __name__ == '__main__':
    unittest.main()