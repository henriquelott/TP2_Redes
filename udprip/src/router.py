import socket
import json
import sys
import time
import threading
from commands import process_command
from topology import Topology

class Router:
    def __init__(self, address, period):
        self.address = address
        self.period = period
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.topology = Topology(self.socket, self.period)
        self.socket.bind((address, 55151))
        self.running = True

    def start(self):
        threading.Thread(target=self.receive_messages, daemon=True).start()
        threading.Thread(target=self.send_periodic_updates, daemon=True).start()
        self.command_interface()

    def receive_messages(self):
        while self.running:
            data, addr = self.socket.recvfrom(1024)
            message = json.loads(data.decode())
            self.topology.process_message(message)

    def send_periodic_updates(self):
        while self.running:
            self.topology.send_updates()
            time.sleep(self.period)

    def command_interface(self):
        while self.running:
            command = input()
            if command.lower() == 'quit':
                self.stop()
            else:
                process_command(self, command) 

    def stop(self):
        self.running = False
        self.socket.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print (sys.argv)
        print("Usage: ./router.py <address> <period> [startup]")
        sys.exit(1)

    address = sys.argv[1]
    period = float(sys.argv[2])
    router = Router(address, period)

    if len(sys.argv) == 4:
        with open(sys.argv[3], 'r') as f:
            for line in f:
                process_command(router, line.strip())

    try:
        router.start()
    except KeyboardInterrupt:
        router.stop()