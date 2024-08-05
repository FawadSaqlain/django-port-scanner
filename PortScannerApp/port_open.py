'''
import socket
import subprocess
import pickle
import time

def run_fake_server(ip, port):
    script_path = 'E:\\one drive\\OneDrive - Happy English\\programms\\web dev\\django\\project1\\django-port-scanner\\PortScannerApp\\fake_server.py'
    process = subprocess.Popen(
        ['python', script_path, ip, str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process

def open_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    try:
        result = sock.connect_ex((ip, port))
        if result == 0:
            return "The port is already opened for any other process"
        else:
            run_fake_server(ip, port)
            return "A new port is opened with fake server"
    except socket.error as err:
        return f"Error: {err}"
    finally:
        sock.close()
'''
import socket
import subprocess

def run_fake_server(ip, port):
    script_path = 'E:\\one drive\\OneDrive - Happy English\\programms\\web dev\\django\\project1\\django-port-scanner\\PortScannerApp\\fake_server.py'
    process = subprocess.Popen(
        ['python', script_path, ip, str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process

def open_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    try:
        result = sock.connect_ex((ip, port))
        if result == 0:
            return "The port is already opened for any other process"
        else:
            run_fake_server(ip, port)
            return "A new port is opened with fake server"
    except socket.error as err:
        return f"Error: {err}"
    finally:
        sock.close()
