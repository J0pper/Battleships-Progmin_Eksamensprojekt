import socket
from _thread import *

# server = "192.168.0.49"
server = socket.gethostbyname(socket.gethostname())
port = 5555

# Create the socket for the server.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)


def read_pos(position: str):
    position = position.split(",")
    return int(position[0]), int(position[1])


def make_pos(position: tuple):
    return f"{position[0]}, {position[1]}"


def threaded_client(connection, player):
    connection.send(str.encode(make_pos(clientPositions[player])))
    reply = ""
    while True:
        try:
            data = read_pos(connection.recv(2048).decode())
            clientPositions[player] = data

            if not data:
                print("Disconnected")
                break

            reply = clientPositions[0] if player == 1 else clientPositions[1]

            print("Received: ", data)
            print("Sending : ", reply)

            connection.sendall(str.encode(make_pos(reply)))
        except socket.error as err:
            print("error occurred in threaded-client", err)
            break

    print("Lost connection")
    connection.close()


s.listen(2)
print("Waiting for a connection, Server Started")

clientPositions: list[tuple[int, int]] = [(0, 0), (100, 100)]

# Amount of players or clients connected to the server.
# Default is 0, but the number increases with one per connected client.
currPlayerAmount: int = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currPlayerAmount))
    currPlayerAmount += 1
