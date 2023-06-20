# car_racing_network.py
import socket
import pickle
import threading

class Network(threading.Thread):
    def __init__(self,*args,**kwargs):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.reciever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.reciever.connect(self.addr)
        self.p = self.connect()
        # self.msg = None
        self.msgs = []
        super(Network,self).__init__(*args,**kwargs)

    def get_p(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            # return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)
            
    def send_chat(self, message):
        try:
            self.client.send(str.encode("chat," + message + "\n"))
            # return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)

    def run(self):
        while True:
            msg = self.reciever.recv(2048).decode()
            # print('rcv messages',msg)
            self.msgs.append(msg)
