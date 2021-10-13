import socket

HOST = "127.0.0.1"
PORT = 9000

with socket.socket() as server_sock:
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_sock.bind((HOST, PORT))

    server_sock.listen(0)
    print(f"Listening on {HOST}:{PORT}...")