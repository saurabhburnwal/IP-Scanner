import socket
import time
import threading
from queue import Queue

socket.setdefaulttimeout(0.25)
print_lock = threading.Lock()

target = input("Enter the IP address to scan: ")
t_IP = socket.gethostbyname(target)
print("Starting scan on host: ", t_IP)

def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((t_IP, port))
        with print_lock:
            print(port, "is open")
        con.close()
    except:
        pass

def threader():
    while True:
        worker = q.get()
        portscan(worker)
        q.task_done()

q = Queue()
