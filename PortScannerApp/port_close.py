import socket
import psutil

def is_port_open(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex((ip, port))
            return result == 0
    except Exception as e:
        return f"Error occurred while checking port status: {e}"

def find_and_terminate_process_using_port(port):
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                for conn in proc.connections(kind='inet'):
                    if conn.laddr.port == port:
                        find_and_terminate_process_using_port_message = f"Terminating process {proc.info['name']} (PID {proc.info['pid']}) using port {port}."
                        proc.terminate()
                        proc.wait()
                        return True, find_and_terminate_process_using_port_message
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False, "No process found using port or could not terminate it."
    except Exception as e:
        return False, f"Error occurred while terminating process: {e}"

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
    try:
        port_close_list = []
        if is_port_open(ip_address, port_number):
            port_close_list.append(f"Port {port_number} on {ip_address} is open.")
            success, message = find_and_terminate_process_using_port(port_number)
            if success:
                port_close_list.append(message)
                port_close_list.append(f"Process using port {port_number} terminated.")
                port_close_list.append(attempt_to_bind_port(ip_address, port_number))
            else:
                port_close_list.append(message)
        else:
            port_close_list.append(f"Port {port_number} on {ip_address} is already closed or not reachable.")
        return port_close_list
    except Exception as e:
        return [f"An error occurred: {e}"]
