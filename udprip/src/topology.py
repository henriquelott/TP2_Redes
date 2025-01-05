import json
import threading

class Topology:
    def __init__(self, socket, period):
        self.routing_table = {}
        self.neighbors = {}
        self.period = period
        self.socket = socket
        self.timers = {}

    def add_link(self, ip, weight):
        if ip not in self.routing_table:
            self.neighbors[ip] = weight
            self.routing_table[ip] = {ip: weight}
        
        self.set_timer(ip)

    def get_weight(self, ip):
        return list(self.routing_table[ip].values())[0]

    def set_timer(self, ip):
        if ip in self.timers.keys() and self.timers[ip] is not None:
            self.timers[ip].cancel()
            print(f"Timer for {ip} canceled")
        self.timers[ip] = threading.Timer(4*self.period, self.remove_link, args=[ip])
        self.timers[ip].start()

    def remove_link(self, ip):
        if ip in self.routing_table:
            del self.neighbors[ip]
            del self.routing_table[ip]
            del self.timers[ip]
        
        list_keys = list(self.routing_table.keys())
        
        for key in list_keys:
            if ip in self.routing_table[key].keys():
                del self.routing_table[key]
        print(f"Routes learned from {ip} have been removed.")

    def update_routing_table(self, table, neighbor):
        # Update the routing table based on the current neighbors
        for ip, weight in table.items():
            if ip != self.socket.getsockname()[0]:
                if neighbor in self.neighbors.keys():
                    neighbor_weight = self.get_weight(neighbor)
                    weight = weight + neighbor_weight
                    
                    if ip in self.routing_table.keys():
                        current_weight = self.get_weight(ip)
                        current_weight = current_weight + neighbor_weight 
                    else:
                        current_weight = weight
                    
                    if ip not in self.routing_table.keys() or weight < current_weight:
                        self.routing_table[ip] = {neighbor: weight}

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
        
        print(self.routing_table)


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
        
        if source in self.neighbors.keys():
            self.set_timer(source)
        else:
            print (f"Received update from {source} wich is not a neighbor")
        
        self.update_routing_table(distances, source)
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