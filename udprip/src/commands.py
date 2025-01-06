def add_link(router, ip, weight):
    router.topology.add_link(ip, weight)

def del_link(router, ip):
    router.topology.remove_link(ip)

def trace_route(router, ip):
    route = router.topology.get_best_route(ip)
    router.topology.trace_message(ip)
    if route is not None:
        print(f"Best route to {ip} is through {route}.")
    else:
        print(f"No route found to {ip}.")

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
    elif cmd == 'quit' and len(parts) == 1:
        router.stop()
    else:
        print("Invalid command")