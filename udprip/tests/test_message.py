import json
import unittest
from src.message import create_message, parse_message

class TestMessage(unittest.TestCase):

    def test_create_data_message(self):
        message = create_message("data", "127.0.1.1", "127.0.1.2", "Hello, World!")
        expected = {
            "type": "data",
            "source": "127.0.1.1",
            "destination": "127.0.1.2",
            "payload": "Hello, World!"
        }
        self.assertEqual(message, expected)

    def test_create_update_message(self):
        distances = {"127.0.1.2": 10, "127.0.1.3": 20}
        message = create_message("update", "127.0.1.1", "127.0.1.2", distances=distances)
        expected = {
            "type": "update",
            "source": "127.0.1.1",
            "destination": "127.0.1.2",
            "distances": distances
        }
        self.assertEqual(message, expected)

    def test_create_trace_message(self):
        message = create_message("trace", "127.0.1.1", "127.0.1.2", routers=["127.0.1.1"])
        expected = {
            "type": "trace",
            "source": "127.0.1.1",
            "destination": "127.0.1.2",
            "routers": ["127.0.1.1"]
        }
        self.assertEqual(message, expected)

    def test_parse_message(self):
        json_message = json.dumps({
            "type": "data",
            "source": "127.0.1.1",
            "destination": "127.0.1.2",
            "payload": "Hello, World!"
        })
        parsed = parse_message(json_message)
        expected = {
            "type": "data",
            "source": "127.0.1.1",
            "destination": "127.0.1.2",
            "payload": "Hello, World!"
        }
        self.assertEqual(parsed, expected)

if __name__ == '__main__':
    unittest.main()