import socket


def receive_file(ip):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((ip, 5000))

    header = b""

    while not header.endswith(b"\n"):
        header += client.recv(1)

    filename, filesize = (
        header.decode().strip().split("|")
    )

    filesize = int(filesize)

    print("Filename:", filename)
    print("Filesize:", filesize)

    data = b""

    while len(data) < filesize:
        packet = client.recv(4096)

        if not packet:
            break

        data += packet

    client.close()

    return filename, data