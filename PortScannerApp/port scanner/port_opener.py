import socket
from threading import Thread, Event

def scan_port(ip, port):
    # Create a new socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Set a timeout for the connection attempt

    try:
        # Try to connect to the target IP and port
        result = sock.connect_ex((ip, port))
        if result == 0:
            return (f"Port {port} is open", [])
        else:
            open_port_result, connections = open_closed_port(ip, port)  # Attempt to open the closed port
            return (f"Port {port} is closed. {open_port_result}", connections)
    except socket.error as err:
        return (f"Error: {err}", [])
    finally:
        sock.close()  # Always close the socket after use

def open_closed_port(ip, port):
    fake_server_Result_Return_list = []
    fake_server_event = Event()

    # Function to open a closed port by creating a fake server
    def fake_server():
        try:
            fake_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            fake_socket.bind((ip, port))
            fake_socket.listen(1)
            fake_server_Result_Return_list.append(f"Fake server started on port {port}")
            fake_server_event.set()  # Notify that the server has started
            while True:
                conn, addr = fake_socket.accept()
                fake_server_Result_Return_list.append(f"Connection established with {addr}")
                conn.close()
        except Exception as e:
            fake_server_Result_Return_list.append(f"Error occurred while opening port: {e}")

    # Start the fake server in a separate thread
    fake_server_thread = Thread(target=fake_server)
    fake_server_thread.start()

    # Wait for the server to start
    fake_server_event.wait()

    return (f"Fake server started on port {port}", fake_server_Result_Return_list)

if __name__ == "__main__":
    ip_address = input("Enter the IP address: ")
    port_number = int(input("Enter the port number: "))
    result, connections = scan_port(ip_address, port_number)
    # print(result)
    if connections:
        for connection in connections:
            print(connection)
