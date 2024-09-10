import socket
import time
import threading
from queue import Queue

socket.setdefaulttimeout(0.25)
print_lock = threading.Lock()

target = input("Enter the IP address to scan: ")
t_IP = socket.gethostbyname(target)
print("Starting scan on host: ", t_IP)
