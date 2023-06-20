from _thread import *
import socket
import pickle
import random
import time

class Server:
    def __init__(self):
        self.server = '0.0.0.0'
        self.port = 5555
        self.addr = (self.server, self.port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.recievers = []
        self.car_game_states = [[0, 0], [0, 0]]
        self.enemy_car_state = {"startx": random.randrange(310, 450), "starty": -600, "speed": 5}

    def start(self):
        self.s.bind(self.addr)
        self.s.listen(2)  # Listen for up to 2 connections
        print('Server Started. Waiting for connections...')

        while True:
            
            conn2, addr2 = self.s.accept()  # Accept a connection
            self.recievers.append(conn2)

            conn, addr = self.s.accept()  # Accept a connection
            print(f'Connected to: {addr}')
            self.clients.append(conn)

            # Only start game when 2 clients have connected
            if len(self.clients) == 2:
                print("Starting game!")
                for i in range(2):
                    start_new_thread(self.threaded_client, (self.clients[i], i))
                
                start_new_thread(self.thread_enemy,())

    def thread_enemy(self):
        while True:
            # self.enemy_car_state["starty"] += self.enemy_car_state["speed"]
            # if self.enemy_car_state["starty"] > 600:  # Assuming 600 is the display height
                # self.enemy_car_state["starty"] = 0 - 100  # Assuming 100 is the enemy car height
                rand_enemy = random.randrange(310, 450)                    
            
                msg = f'enemey,{rand_enemy},{-100},{self.enemy_car_state["speed"]}'
                for reciever in self.recievers:
                    reciever.send(msg.encode('utf-8'))
                time.sleep(2)

    def threaded_client(self, conn, player):
        conn.send(str.encode(str(player)))
        reply = ""

        while True:
            try:
                data = conn.recv(2048 * 2)
                reply = data.decode("utf-8")
                print(reply)
                if not data:
                    print("Player", player, "disconnected")
                    break
                else:
                    
                       

                    if reply.startswith("update"):
                        _, _ ,x = reply.split(',')
                        x = float(x)                    
                        self.car_game_states[player] = [x,0]
                        if player == 0:
                            self.car_game_states[0] = reply
                            msg = f'update,{player},{x}'
                            for reciever in self.recievers:
                                reciever.send(msg.encode('utf-8'))
                        elif player == 1:
                            self.car_game_states[1] = reply
                            msg = f'update,{player},{x}'
                            for reciever in self.recievers:
                                reciever.send(msg.encode('utf-8'))
                            # self.recievers[0].send(msg.encode('utf-8'))
                    
                    elif reply.startswith("chat"):
                        chat_message = reply.split(",", 1)[1]
                        if player == 0:
                            self.car_game_states[0] = reply
                            msg = f'chat,{chat_message}'
                            for reciever in self.recievers:
                                reciever.send(msg.encode('utf-8'))
                            # self.recievers[1].send(msg.encode('utf-8'))
                        elif player == 1:
                            self.car_game_states[1] = reply
                            msg = f'chat,{chat_message}'
                            for reciever in self.recievers:
                                reciever.send(msg.encode('utf-8'))
                            # self.recievers[1].send(msg.encode('utf-8'))
                    elif reply.startswith("quit"):
                        msg = f'quit,{player}'
                        for reciever in self.recievers:
                            reciever.send(msg.encode('utf-8'))


            except ConnectionResetError:
                print("Player", player, "disconnected")
                conn.close()
                self.clients.remove(conn)
                break



        # Check if the other player is still connected
        if len(self.clients) == 1:
            remaining_player = 0 if player == 1 else 1
            print("Player", remaining_player, "wins!")

            # Send winning message to the remaining player
            self.clients[0].send(f'quit,{remaining_player}')

server = Server()
server.start()
