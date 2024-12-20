import unittest
from src.router import Router

class TestRouter(unittest.TestCase):

    def setUp(self):
        self.router = Router("127.0.1.5", 1)

    def test_initialization(self):
        self.assertEqual(self.router.address, "127.0.1.5")
        self.assertEqual(self.router.period, 1)
        self.assertEqual(self.router.routing_table, {})
        self.assertEqual(self.router.neighbors, {})

    def test_add_link(self):
        self.router.add_link("127.0.1.1", 10)
        self.assertIn("127.0.1.1", self.router.neighbors)
        self.assertEqual(self.router.neighbors["127.0.1.1"], 10)

    def test_remove_link(self):
        self.router.add_link("127.0.1.1", 10)
        self.router.remove_link("127.0.1.1")
        self.assertNotIn("127.0.1.1", self.router.neighbors)

    def test_route_update(self):
        self.router.add_link("127.0.1.1", 10)
        self.router.update_routes({"127.0.1.2": 20})
        self.assertEqual(self.router.routing_table["127.0.1.2"], 30)

    def test_forward_data(self):
        self.router.add_link("127.0.1.1", 10)
        self.router.routing_table = {"127.0.1.1": 10}
        result = self.router.forward_data("127.0.1.1", "Test payload")
        self.assertEqual(result, "Data sent to 127.0.1.1: Test payload")

    def test_forward_data_no_route(self):
        result = self.router.forward_data("127.0.1.2", "Test payload")
        self.assertEqual(result, "No route to 127.0.1.2")

if __name__ == '__main__':
    unittest.main()