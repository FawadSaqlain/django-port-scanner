import socket
import pickle
import sys
from threading import Thread, Event

def fake_server(ip, port, result_list, event):
    try:
        fake_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fake_socket.bind((ip, port))
        fake_socket.listen(1)
        result_list.append(f"Fake server started on port {port}")
        event.set()
        while True:
            conn, addr = fake_socket.accept()
            result_list.append(f"Connection established with {addr}")
            conn.close()
    except Exception as e:
        result_list.append(f"Error occurred while opening port: {e}")

if __name__ == "__main__":
    ip = sys.argv[1]
    port = int(sys.argv[2])
    result_list = []
    event = Event()

    server_thread = Thread(target=fake_server, args=(ip, port, result_list, event))
    server_thread.start()
    event.wait()

    print(pickle.dumps(result_list))
