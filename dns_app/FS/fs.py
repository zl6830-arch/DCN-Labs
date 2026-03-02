from flask import Flask, request
import socket

app = Flask(__name__)

def fib(n):
    if n <= 0: return 0
    if n == 1: return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

@app.route('/register', methods=['PUT'])
def register():
    content = request.json
    hostname = content.get('hostname')
    ip = content.get('ip')
    as_ip = content.get('as_ip')
    as_port = int(content.get('as_port'))

    dns_msg = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(dns_msg.encode(), (as_ip, as_port))
    
    return "Registered successfully", 201

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    number = request.args.get('number')
    try:
        x = int(number)
        return str(fib(x)), 200
    except (TypeError, ValueError):
        return "Bad Request: number must be an integer", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)