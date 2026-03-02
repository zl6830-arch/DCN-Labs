import socket
import os

UDP_IP = "0.0.0.0"
UDP_PORT = 53533
DB_FILE = "dns_records.txt"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Authoritative Server running on UDP port {UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(1024)
    lines = data.decode().strip().split('\n')
    
    if len(lines) >= 4 and lines[0].startswith("TYPE=A"):
        with open(DB_FILE, "a") as f:
            f.write(data.decode().strip() + "\n---\n")
    
    elif len(lines) >= 2 and lines[0].startswith("TYPE=A"):
        target_name = lines[1]
        response = ""
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r") as f:
                records = f.read().split('---\n')
                for record in records:
                    if target_name in record:
                        response = record.strip()
                        break
        if response:
            sock.sendto(response.encode(), addr)