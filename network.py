import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        if self.p is None:#Ensures that getP() returns valid data and not handles it gracefully
            print("Error: No data received from server")
        return self.p


    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except Exception as e:
            print(e)
            return None
        
    def send(self, data):
        try:
            # Convert data to dictionary if it's an instance of Player
            if hasattr(data, '__dict__'):
                data = data.__dict__
            self.client.send(pickle.dumps(data))  # Send data as dictionary
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(f"Socket erorr: {e}")
            return None

        

