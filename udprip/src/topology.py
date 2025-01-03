import json

class Topology:
    def __init__(self, socket):
        self.routing_table = {}
        self.neighbors = {}
        self.socket = socket

    def add_link(self, ip, weight):
        if ip not in self.neighbors:
            self.neighbors[ip] = weight
            self.update_routing_table(ip, weight)

    def remove_link(self, ip):
        if ip in self.neighbors:
            del self.neighbors[ip]
            self.update_routing_table(ip, float('inf'))

    def update_routing_table(self, ip, weight):
        # Update the routing table based on the current neighbors
        for neighbor in self.neighbors:
            if neighbor not in self.routing_table or self.routing_table[neighbor] > weight:
                self.routing_table[neighbor] = weight

    def get_best_route(self, destination):
        return self.routing_table.get(destination, None)

    def get_neighbors(self):
        return self.neighbors.keys()
    
    def send_updates(self):
        update_message = {
            "type": "update",
            "source": self.socket.getsockname()[0],
            "distances": self.routing_table
        }
        for neighbor in self.neighbors:
            update_message["destination"] = neighbor
            self.socket.sendto(json.dumps(update_message).encode(), (neighbor, 55151))
            
    def process_message(self, message):
        if message["type"] == "update":
            self.handle_update_message(message)
        elif message["type"] == "data":
            self.handle_data_message(message)
        elif message["type"] == "trace":
            self.handle_trace_message(message)

    def handle_update_message(self, message):
        source = message["source"]
        distances = message["distances"]
        for destination, distance in distances.items():
            if destination not in self.routing_table or self.routing_table[destination] > distance:
                self.routing_table[destination] = distance
                self.neighbors[source] = distance

    def handle_data_message(self, message):
        destination = message["destination"]
        if destination == self.socket.getsockname()[0]:
            print(message)
        else:
            next_hop = destination
            if next_hop:
                self.socket.sendto(json.dumps(message).encode(), (next_hop, 55151))

    def handle_trace_message(self, message):
        message["routers"].append(self.socket.getsockname()[0])
        if message["destination"] == self.socket.getsockname()[0]:
            response = {
                "type": "data",
                "source": self.socket.getsockname()[0],
                "destination": message["source"],
                "payload": json.dumps(message)
            }
            self.socket.sendto(json.dumps(response).encode(), (message["source"], 55151))
        else:
            next_hop = message["destination"]
            if next_hop:
                self.socket.sendto(json.dumps(message).encode(), (next_hop, 55151))
    
    def trace_message(self, destination):
        trace_message = {
            "type": "trace",
            "source": self.socket.getsockname()[0],
            "destination": destination,
            "routers": []
        }
        self.handle_trace_message(trace_message)