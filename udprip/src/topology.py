import json
import threading

class Topology:
    def __init__(self, socket, period, address):
        self.routing_table = {}
        self.neighbors = {}
        self.period = period
        self.socket = socket
        self.address = address
        self.timers = {}

    def add_link(self, ip, weight, neighbor=None):
        if neighbor is None:
            self.neighbors[ip] = weight
            self.set_timer(ip)
            self.routing_table[ip] = {ip: weight}
        else:
            self.routing_table[ip] = {neighbor: weight}
        
        self.send_updates()

    def get_weight(self, ip):
        return list(self.routing_table[ip].values())[0]

    def set_timer(self, ip):
        if ip in self.timers.keys() and self.timers[ip] is not None:
            self.timers[ip].cancel()
        self.timers[ip] = threading.Timer(4*self.period, self.remove_link, args=[ip])
        self.timers[ip].start()

    def remove_link(self, ip):
        if ip in self.routing_table.keys():
            del self.routing_table[ip]
            
            if ip in self.neighbors.keys():
                del self.neighbors[ip]
                
                if self.timers[ip] is not None:
                    del self.timers[ip]
        
        list_keys = list(self.routing_table.keys())
        
        for key in list_keys:
            if ip in self.routing_table[key].keys():
                del self.routing_table[key]
        self.send_updates()

    def update_routing_table(self, table, neighbor):
        # Update the routing table based on the current neighbors
        for ip, weight in table.items():
            if ip != self.address:
                if neighbor in self.neighbors.keys():
                    neighbor_weight = self.get_weight(neighbor)
                else:
                    neighbor_weight = 0
                
                weight = weight + neighbor_weight
                
                if ip in self.routing_table.keys():
                    current_weight = self.get_weight(ip)
                else:
                    current_weight = weight
                
                if ip not in self.routing_table.keys() or weight < current_weight:
                    self.add_link(ip, weight, neighbor)
        
        list_links = list(self.routing_table.keys())
        ips = list(table.keys())
        for link in list_links:
            if (neighbor in self.routing_table[link].keys()) and (link not in ips) and (link != neighbor):
                self.remove_link(link)

    def get_best_route(self, destination):
        if destination not in self.routing_table.keys():
            return None
        else:
            return list(self.routing_table[destination].keys())[0]

    def get_neighbors(self):
        return self.neighbors.keys()
    
    def send_updates(self):
        distances = {}
        for routers in self.routing_table.keys():
            distances[routers] = self.get_weight(routers)
        
        update_message = {
            "type": "update",
            "source": self.address,
            "distances": distances
        }
        neighbors = list(self.neighbors.keys())
        for neighbor in neighbors:
            if neighbor in self.neighbors.keys():
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
        
        if source in self.neighbors.keys():
            self.set_timer(source)
            self.update_routing_table(distances, source)

    def handle_data_message(self, message):
        destination = message["destination"]
        if destination == self.address:
            payload = json.loads(message["payload"])
            print(json.dumps(payload, indent=4))
        else:
            next_hop = destination
            if next_hop:
                self.socket.sendto(json.dumps(message).encode(), (next_hop, 55151))

    def handle_trace_message(self, message):
        if message["source"] in self.routing_table.keys() or message["source"] == self.address:
            message["routers"].append(self.address)
            if message["destination"] == self.address:
                response = {
                    "type": "data",
                    "source": self.address,
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
        if destination not in self.routing_table.keys():
            return
        else:
            trace_message = {
                "type": "trace",
                "source": self.address,
                "destination": destination,
                "routers": []
            }
            self.handle_trace_message(trace_message)