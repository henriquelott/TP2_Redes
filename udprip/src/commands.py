def add_link(router, ip, weight):
    # Logic to add a link to the router's topology
    pass

def del_link(router, ip):
    # Logic to delete a link from the router's topology
    pass

def trace_route(router, ip):
    # Logic to initiate a trace route to the specified IP
    pass

def process_command(router, command):
    parts = command.split()
    if not parts:
        return

    cmd = parts[0]
    if cmd == 'add' and len(parts) == 3:
        ip = parts[1]
        weight = int(parts[2])
        add_link(router, ip, weight)
    elif cmd == 'del' and len(parts) == 2:
        ip = parts[1]
        del_link(router, ip)
    elif cmd == 'trace' and len(parts) == 2:
        ip = parts[1]
        trace_route(router, ip)
    else:
        print("Invalid command")