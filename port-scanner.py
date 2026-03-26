import socket
import threading
from datetime import datetime

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            try:
                banner = sock.recv(1024).decode().strip()
                return f"Port {port} OPEN - Banner: {banner[:100]}"
            except:
                return f"Port {port} OPEN"
        sock.close()
    except:
        pass
    return None

def main():
    print("Simple Port Scanner")
    target = input("Enter target IP or domain: ").strip()
    start_port = int(input("Start port (default 1): ") or 1)
    end_port = int(input("End port (default 1000): ") or 1000)
    
    print(f"\nScanning {target} from port {start_port} to {end_port}...")
    print(f"Start time: {datetime.now()}\n")
    
    open_ports = []
    threads = []
    
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=lambda p=port: open_ports.append(scan_port(target, p)))
        threads.append(thread)
        thread.start()
        
        # Limit threads to avoid overwhelming the network
        if len(threads) >= 100:
            for t in threads:
                t.join()
            threads = []
    
    for t in threads:
        t.join()
    
    open_ports = [p for p in open_ports if p]
    for result in open_ports:
        print(result)
    
    print(f"\nScan completed at {datetime.now()}")
    print(f"Found {len(open_ports)} open ports.")

if __name__ == "__main__":
    main()
