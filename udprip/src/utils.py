def log_message(message):
    print(f"[LOG] {message}")

def handle_error(error_message):
    print(f"[ERROR] {error_message}")

def parse_command(command):
    return command.strip().split()