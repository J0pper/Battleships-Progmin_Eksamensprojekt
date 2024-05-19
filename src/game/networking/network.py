import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates a new socket per client.
        # self.server = socket.gethostbyname(socket.gethostname())  # Grabs your local IPv4 address.
        self.server: str = input("Server IP-address here: ")
        self.port: int = int(input("Port here: "))  # Specify a free port on your internet connection.
        self.connectMessage: str = self.connect_server()  # Connects the client socket with the server.

    # Passer function.
    # Might be useful, might need to be deleted.
    def get_connection_message(self) -> str:
        return self.connectMessage

    def connect_server(self) -> str:
        """
        This function lets a client socket connect to a localhost server.
        Firstly the client socket connects to the network IP on the specified port.
        After which the initially sent message I caught and returned.

        If something fails, the error is caught and printed to the terminal.

        :return: Returns the initially send message as a string.
        """
        try:
            self.client.connect((self.server, self.port))  # Connect to server.
            return self.client.recv(2048).decode()  # Receive and return reply-message as string.
        except socket.error as e:
            print("connect_server failed", e)  # Error-handling.

    def send(self, data):
        """
        Function that allows the user to send data over the network to a server
        and get a reply back.

        In case that something fails, the error is caught and will be printed to the terminal.

        :param data: Data that is wished to be sent to the server.
        :return: Receives a reply-message from the server as a string.
        """
        try:
            self.client.send(pickle.dumps(data))  # Send data to the server as a string.
            return pickle.loads(self.client.recv(2048*2))  # Receive and return reply-message as a string.
        except socket.error as e:
            print("send failed", e)  # Error-handling.
