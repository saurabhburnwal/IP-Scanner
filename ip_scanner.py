import socket
import time
import threading
from queue import Queue

# Set a default socket timeout (can be adjusted by the user)
socket.setdefaulttimeout(0.5)

# Threading Lock
print_lock = threading.Lock()

def get_ip(target):
    try:
        t_IP = socket.gethostbyname(target)
        print(f"Starting scan on host: {t_IP}")
        return t_IP
    except socket.gaierror:
        print("Invalid hostname or IP address.")
        return None

# Port Scanning Function
def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((t_IP, port))
        with print_lock:
            print(port, "is open", socket.getservbyport(port))
        con.close()
    except:
        pass

# Thread Worker Function
def threader():
    while True:
        worker = q.get()
        portscan(worker)
        q.task_done()

# Queue and Threads Setup
q = Queue()

startTime = time.time()

for x in range(100):
    t = threading.Thread(target = threader)
    t.daemon = True
    t.start()

for worker in range(1, 500):
    q.put(worker)

q.join()

# Execution Time
print('Time taken:', time.time() - startTime)