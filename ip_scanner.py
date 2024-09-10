import socket
import time
import threading
from queue import Queue

# Socket and Timeout Setup
socket.setdefaulttimeout(0.25)

# Threading Lock
print_lock = threading.Lock()

# Target IP Setup
target = input("Enter the IP address to scan: ")
t_IP = socket.gethostbyname(target)

print("Starting scan on host: ", t_IP)

# Port Scanning Function
def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((t_IP, port))
        with print_lock:
            print(port, "is open")
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