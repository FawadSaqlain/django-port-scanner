import socket
import psutil

def is_port_open(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex((ip, port))
        return result == 0

def find_and_terminate_process_using_port(port):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == port:
                    # Exclude Django process from termination
                    if "python" in proc.info['name'].lower() and "manage.py" not in proc.info['name'].lower():
                        proc.terminate()
                        proc.wait()  # Wait for the process to be terminated
                        return f"Terminated process {proc.info['name']} (PID {proc.info['pid']})."
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return f"No process found using port {port} or could not terminate it."

def attempt_to_bind_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((ip, port))
            s.listen(1)
            return f"Port {port} on {ip} is now bound to this socket, simulating closure."
    except socket.error as e:
        return f"Error occurred while attempting to bind to port: {e}"


def port_close(ip_address, port_number):
    if is_port_open(ip_address, port_number):
        message = find_and_terminate_process_using_port(port_number)
        if message:
            return [
                f"Port {port_number} on {ip_address} is open.",
                message,
                f"Process using port {port_number} terminated.",
                attempt_to_bind_port(ip_address, port_number),
            ]
        else:
            return [f"No process found using port {port_number} or could not terminate it."]
    else:
        return [f"Port {port_number} on {ip_address} is already closed or not reachable."]

# Example usage:
ip_address = "127.0.0.1"
port_number = 34521  # Adjust to your fake server port
results = port_close(ip_address, port_number)
print("\n".join(results))  # Display the results

