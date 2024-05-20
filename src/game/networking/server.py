import socket
from _thread import *
import pickle
from src.game.board_manager import BoardManager


def start_server():
    ipAddress = socket.gethostbyname(socket.gethostname())  # get local ip-address for the device running the server.
    print("Server IP-address: ", ipAddress)
    portRange = [5000, 7000]  # specify a range within to check for available ports.
    port = portRange[0]

    # Create the socket for the server.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Try binding to a port until it succeeds, then break the while loop.
    binding = True
    while binding:
        try:
            s.bind((ipAddress, port))
            binding = False
            print("Server port: ", port)
        except socket.error as e:
            if port != portRange[1]:
                port += 1
                continue
            print("no ports available", e)

    # Tell the socket to only listen for two connections.
    s.listen(2)
    print("Waiting for a connection, Server Started")

    # Amount of players or clients connected to the server.
    # Default is 0, but the number increases with one per connected client.
    currPlayerAmount: int = 0
    boardManager = BoardManager()  # Holds a BoardManager-object.
    while True:
        # Accept a connection to the socket.
        conn, addr = s.accept()  # Returns a new socket representing the connection, and the address of the client.
        print("Connected to:", addr)

        # Set the connectReady variable to true when to players have connected.
        if currPlayerAmount % 2 == 1:
            boardManager.connectReady = True

        # Start a new thread and supply it with a function to run.
        start_new_thread(threaded_client, (conn, currPlayerAmount, boardManager))
        currPlayerAmount += 1


def threaded_client(connection, player, board_manager):
    connection.send(str.encode(str(player)))  # Send the player number to the player.

    while True:
        try:
            data = pickle.loads(connection.recv(4096*8))  # Try to retrieve and load data.
            if not data:
                print("Didn't receive data. Disconnected as a result.")
                break
            # Check what the data was.
            if data[0] == "ready":
                board_manager.ready(player, data[1])
            if data == "flip_turn":
                board_manager.flip_turn()
            if data != "get":
                board_manager.update_boards(player, data)
            connection.sendall(pickle.dumps(board_manager))  # Send a pickled BoardManager-object.

        # Handle errors
        except socket.error as err:
            print("Error occurred in threaded-client", err)
            break

    print("Lost connection")
    connection.close()  # Close the client socket.


start_server()
