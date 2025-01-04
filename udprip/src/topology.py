import json

class Topology:
    def __init__(self, socket):
        self.routing_table = {}
        self.neighbors = {}
        self.socket = socket

    def add_link(self, ip, weight):
        if ip not in self.routing_table:
            self.neighbors[ip] = weight
            self.routing_table[ip] = {ip: weight}

    def get_weight(self, ip):
        return list(self.routing_table[ip].values())[0]

    def remove_link(self, ip):
        if ip in self.routing_table:
            del self.neighbors[ip]
            del self.routing_table[ip]

    def update_routing_table(self, ip, weight, intermediary):
        # Update the routing table based on the current neighbors
        if ip in self.routing_table:
            intermediary_weight = self.get_weight(intermediary)
            current_weight = self.get_weight(ip)
            current_weight = current_weight + intermediary_weight 
        
        if ip not in self.routing_table.keys() or current_weight < weight:
            self.routing_table[ip] = {intermediary: weight}

    def get_best_route(self, destination):
        return list(self.routing_table[destination].keys())[0]

    def get_neighbors(self):
        return self.neighbors.keys()
    
    def send_updates(self):
        distances = {}
        for routers in self.routing_table.keys():
            distances[routers] = self.get_weight(routers)
        
        update_message = {
            "type": "update",
            "source": self.socket.getsockname()[0],
            "distances": distances
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
        for ips, distance in distances.items():
            if ips != self.socket.getsockname()[0]:
                self.update_routing_table(ips, distance, source)
        print(message)

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
            destination = self.get_best_route(message["source"])
            self.socket.sendto(json.dumps(response).encode(), (destination, 55151))
        else:
            next_hop = self.get_best_route(message["destination"])
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