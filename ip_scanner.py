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
def portscan(t_IP, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((t_IP, port))
        with print_lock:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown service"
            print(f"Port {port} is open ({service})")
        con.close()
    except:
        pass

# Thread Worker Function
def threader(t_IP):
    while True:
        worker = q.get()
        portscan(worker)
        q.task_done()

def main():
    # Get user input for target and port range
    target = input("Enter the IP address or hostname to scan: ")
    t_IP = get_ip(target)
    if not t_IP:
        return  # Exit if the IP address is invalid
    
    try:
        start_port = int(input("Enter the start port (e.g., 1): "))
        end_port = int(input("Enter the end port (e.g., 500): "))
        if start_port < 1 or end_port > 65535 or start_port > end_port:
            print("Invalid port range. Please enter valid port numbers between 1 and 65535.")
            return
    except ValueError:
        print("Invalid input for port numbers. Please enter valid integers.")
        return

    # Option to adjust timeout
    try:
        timeout = float(input("Enter timeout in seconds (default 0.5): ") or "0.5")
        socket.setdefaulttimeout(timeout)
    except ValueError:
        print("Invalid input for timeout. Using default of 0.5 seconds.")
        timeout = 0.5
    

    # Queue and threading setup
    global q
    q = Queue()

    startTime = time.time()

    # Start threads
    for x in range(100):
        t = threading.Thread(target=lambda: threader(t_IP))
        t.daemon = True
        t.start()

    # Add ports to the queue
    for worker in range(start_port, end_port + 1):
        q.put(worker)

     q.join()

    print('Time taken:', time.time() - startTime)

if __name__ == "__main__":
    main()