class Topology:
    def __init__(self):
        self.routing_table = {}
        self.neighbors = {}

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