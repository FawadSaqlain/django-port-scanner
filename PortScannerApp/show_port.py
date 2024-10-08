import socket
import psutil
def scan_port(ip, port):
    # Create a new socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Set a timeout for the connection attempt

    try:
        # Try to connect to the target IP and port
        result = sock.connect_ex((ip, port))
        if result == 0:
            return(f"Port {port} is open")
        else:
            return(f"Port {port} is closed")
    except socket.error as err:
        return(f"Error: {err}")
    finally:
        sock.close()  # Always close the socket after use

def get_process_info(port):
    for conn in psutil.net_connections(kind="inet"):
        if conn.laddr.port == port:
            return f"Process ID: {conn.pid}, Name: {psutil.Process(conn.pid).name()}"
    return "No process found"

