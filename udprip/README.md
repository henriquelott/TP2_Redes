# UDPRIP: Distance Vector Routing Protocol

## Overview
UDPRIP is a routing software that implements the Distance Vector Routing Protocol using UDP sockets. It allows for the creation of a virtual topology of routers that can communicate with each other, manage link weights, and handle route measurements.

## Project Structure
The project is organized as follows:

```
udprip/
├── src/
│   ├── router.py        # Main entry point for the UDPRIP routing software
│   ├── commands.py      # Command handling for 'add', 'del', and 'trace'
│   ├── message.py       # Message encoding and decoding
│   ├── topology.py      # Virtual topology management and routing algorithm
│   └── utils.py         # Utility functions for logging and error handling
├── tests/
│   ├── test_router.py   # Unit tests for router functionality
│   ├── test_commands.py  # Tests for command handling
│   ├── test_message.py   # Tests for message encoding/decoding
│   ├── test_topology.py  # Tests for topology management
│   └── test_utils.py     # Tests for utility functions
├── lo-addresses.sh       # Script to manage loopback interface IP addresses
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
└── startup.txt           # Initial commands for router setup
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd udprip
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Add IP addresses to the loopback interface using the provided `lo-addresses.sh` script:
   ```
   bash lo-addresses.sh
   ```

## Usage
To start a router instance, use the following command:
```
python src/router.py <address> <period> [startup]
```
- `<address>`: The IP address to bind the router to (e.g., 127.0.1.1).
- `<period>`: The time interval (in seconds) for sending routing updates.
- `[startup]`: (Optional) A file containing initial commands for setting up the router's topology.

## Example
To create a simple topology, execute the following commands in the respective routers:
```
# On router 127.0.1.5
add 127.0.1.1 10
add 127.0.1.2 10
add 127.0.1.3 10
add 127.0.1.4 10

# On other routers
add 127.0.1.5 10
```

GAY

## Protocol Features
- **Distance Vector Routing**: Routers exchange routing information to compute the best paths to destinations.
- **Link Weights**: Each link can have a weight that influences route selection.
- **Message Types**: Supports data, update, and trace messages for communication between routers.

## Testing
Run the unit tests to ensure functionality:
```
pytest tests/
```

## Contribution
Feel free to contribute to the project by submitting issues or pull requests.
