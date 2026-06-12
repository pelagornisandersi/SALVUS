import socket
import os

HOST = "0.0.0.0"
PORT = 5000


def start_sender(filename, encrypted_data):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))
    server.listen(1)

    print("Waiting for receiver...")

    conn, addr = server.accept()

    print("Connected:", addr)

    filesize = len(encrypted_data)

    header = f"{os.path.basename(filename)}|{filesize}\n"

    conn.sendall(header.encode())

    conn.sendall(encrypted_data)

    conn.close()
    server.close()