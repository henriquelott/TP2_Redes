import unittest
from src.commands import add_link, remove_link, trace_route

class TestCommands(unittest.TestCase):

    def setUp(self):
        self.router = {
            'ip': '127.0.1.5',
            'links': {},
            'routing_table': {}
        }

    def test_add_link(self):
        add_link(self.router, '127.0.1.1', 10)
        self.assertIn('127.0.1.1', self.router['links'])
        self.assertEqual(self.router['links']['127.0.1.1'], 10)

    def test_remove_link(self):
        add_link(self.router, '127.0.1.1', 10)
        remove_link(self.router, '127.0.1.1')
        self.assertNotIn('127.0.1.1', self.router['links'])

    def test_trace_route(self):
        add_link(self.router, '127.0.1.1', 10)
        trace_result = trace_route(self.router, '127.0.1.1')
        self.assertIn('127.0.1.1', trace_result['routers'])
        self.assertEqual(trace_result['source'], self.router['ip'])
        self.assertEqual(trace_result['destination'], '127.0.1.1')

if __name__ == '__main__':
    unittest.main()