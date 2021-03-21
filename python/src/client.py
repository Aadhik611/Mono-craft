import socket, time


class app:
    def __init__(self, host, port, end_text):

        self.HOST = host
        self.PORT = port

        self.ENDTEXT = end_text

    def send(self, data):

        send_text = f"{data}{self.ENDTEXT}".encode("UTF-8")

        self.client.sendall(send_text)

    def recv(self, buffer):

        recv_text = self.client.recv(buffer)

        return recv_text

    def connect(self):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.HOST, self.PORT))

    def close(self):

        self.client.close()


# ==========          USAGE          ==========#

# client = app("192.168.100.245", 80, "|")

# client.connect()
# client.send("Sample message")
# time.sleep(0.2)
# client.close()
