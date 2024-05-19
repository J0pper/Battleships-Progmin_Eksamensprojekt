import socket
from _thread import *
import pickle
from src.game.board_manager import BoardManager


def start_server():
    server = socket.gethostbyname(socket.gethostname())
    print("Server IP-address: ", server)
    portRange = [5000, 7000]
    port = portRange[0]
    binding = True

    # Create the socket for the server.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while binding:
        try:
            s.bind((server, port))
            binding = False
            print("Server port: ", port)
        except socket.error as e:
            if port != portRange[1]:
                port += 1
                continue
            print("no ports available", e)

    s.listen(2)
    print("Waiting for a connection, Server Started")

    # Amount of players or clients connected to the server.
    # Default is 0, but the number increases with one per connected client.
    currPlayerAmount: int = 0
    boardManager = None
    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)

        if currPlayerAmount % 2 != 1:
            boardManager = BoardManager()
        else:
            boardManager.connectReady = True

        start_new_thread(threaded_client, (conn, currPlayerAmount, boardManager))
        currPlayerAmount += 1


def threaded_client(connection, player, board_manager):
    connection.send(str.encode(str(player)))

    while True:
        try:
            data = pickle.loads(connection.recv(4096*8))
            # print(pickle.loads(data))
            if not data:
                print("Didn't receive data. Disconnected as a result.")
                break
            if data[0] == "ready":
                board_manager.ready(player, data[1])
            if data == "flip_turn":
                board_manager.flip_turn()
            if data != "get":
                board_manager.update_boards(player, data)
            connection.sendall(pickle.dumps(board_manager))

        except socket.error as err:
            print("Error occurred in threaded-client", err)
            break

    print("Lost connection")
    connection.close()


start_server()
