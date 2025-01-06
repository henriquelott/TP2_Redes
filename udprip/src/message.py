import json

def create_message(message_type, source, destination, payload=None, distances=None, routers=None):
    message = {
        "type": message_type,
        "source": source,
        "destination": destination
    }
    if payload is not None:
        message["payload"] = payload
    if distances is not None:
        message["distances"] = distances
    if routers is not None:
        message["routers"] = routers
    return message

def encode_message(message):
    return json.dumps(message)

def decode_message(encoded_message):
    return json.loads(encoded_message)

def process_message(topology, message):
    if message["type"] == "update":
        topology.handle_update_message(message)
    elif message["type"] == "data":
        topology.handle_data_message(message)
    elif message["type"] == "trace":
        topology.handle_trace_message(message)

def handle_update_message(topology, message):
    source = message["source"]
    distances = message["distances"]
    
    if source in topology.neighbors.keys():
        topology.set_timer(source)
        topology.update_routing_table(distances, source)
    else:
        print (f"Received update from {source} wich is not a neighbor")

def handle_data_message(topology, message):
    destination = message["destination"]
    if destination == topology.address:
        print(message)
    else:
        next_hop = destination
        if next_hop:
            topology.socket.sendto(json.dumps(message).encode(), (next_hop, 55151))

def handle_trace_message(topology, message):
    message["routers"].append(topology.address)
    if message["destination"] == topology.address:
        response = {
            "type": "data",
            "source": topology.address,
            "destination": message["source"],
            "payload": json.dumps(message)
        }
        destination = topology.get_best_route(message["source"])
        topology.socket.sendto(json.dumps(response).encode(), (destination, 55151))
    else:
        next_hop = topology.get_best_route(message["destination"])
        if next_hop:
            topology.socket.sendto(json.dumps(message).encode(), (next_hop, 55151))

def trace_message(topology, destination):
    trace_message = {
        "type": "trace",
        "source": topology.address,
        "destination": destination,
        "routers": []
    }
    topology.handle_trace_message(trace_message)