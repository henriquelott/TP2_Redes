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
    import json
    return json.dumps(message)

def decode_message(encoded_message):
    import json
    return json.loads(encoded_message)