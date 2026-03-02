from flask import Flask, request
import socket
import requests

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def handle_user():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not all([hostname, fs_port, number, as_ip, as_port]):
        return "Bad Request", 400

    dns_query = f"TYPE=A\nNAME={hostname}"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5.0)
    
    try:
        sock.sendto(dns_query.encode(), (as_ip, int(as_port)))
        data, _ = sock.recvfrom(1024)
        
        response_lines = data.decode().split('\n')
        fs_ip = ""
        for line in response_lines:
            if line.startswith("VALUE="):
                fs_ip = line.split("=")[1]
                break
        
        if not fs_ip:
            return "DNS Resolution Failed", 500

        fs_url = f"http://{fs_ip}:{fs_port}/fibonacci?number={number}"
        fs_response = requests.get(fs_url)
        
        if fs_response.status_code == 200:
            return fs_response.text, 200
        else:
            return "Error from FS", fs_response.status_code

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)