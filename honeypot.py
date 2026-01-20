# simple_honeypot.py
import socket
import datetime

HOST = "0.0.0.0"
PORT = 2222  # fake SSH port

log_file = "honeypot.log"

def log(data):
    with open(log_file, "a") as f:
        f.write(data + "\n")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print(f"[+] Honeypot listening on {PORT}")

while True:
    conn, addr = s.accept()
    ip = addr[0]
    time = datetime.datetime.utcnow().isoformat()

    log(f"[{time}] Connection from {ip}")
    conn.send(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu\r\n")

    try:
        data = conn.recv(1024).decode(errors="ignore")
        log(f"[{time}] {ip} sent: {data.strip()}")

        # Fake interaction
        conn.send(b"login as: root\npassword: ")
        pwd = conn.recv(1024).decode(errors="ignore")
        log(f"[{time}] {ip} password attempt: {pwd.strip()}")

        conn.send(b"Access denied.\n")
    except:
        pass

    conn.close()
