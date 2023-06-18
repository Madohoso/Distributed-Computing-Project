from _thread import *
import socket
import pickle
import random

class Server:
    def __init__(self):
        self.server = '0.0.0.0'
        self.port = 5555
        self.addr = (self.server, self.port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.car_game_states = [[0, 0], [0, 0]]
        self.enemy_car_state = {"startx": random.randrange(310, 450), "starty": -600, "speed": 5}

    def start(self):
        self.s.bind(self.addr)
        self.s.listen(2)  # Listen for up to 2 connections
        print('Server Started. Waiting for connections...')

        while True:
            conn, addr = self.s.accept()  # Accept a connection
            print(f'Connected to: {addr}')
            self.clients.append(conn)

            # Only start game when 2 clients have connected
            if len(self.clients) == 2:
                print("Starting game!")
                for i in range(2):
                    start_new_thread(self.threaded_client, (self.clients[i], i))

    def threaded_client(self, conn, player):
        conn.send(str.encode(str(player)))
        reply = ""

        while True:
            try:
                data = conn.recv(2048 * 2)
                reply = data.decode("utf-8")

                if not data:
                    print("Player", player, "disconnected")
                    break
                else:
                    if player == 0:
                        self.car_game_states[0] = reply
                    elif player == 1:
                        self.car_game_states[1] = reply

                    self.enemy_car_state["starty"] += self.enemy_car_state["speed"]
                    if self.enemy_car_state["starty"] > 600:  # Assuming 600 is the display height
                        self.enemy_car_state["starty"] = 0 - 100  # Assuming 100 is the enemy car height
                        self.enemy_car_state["startx"] = random.randrange(310, 450)
                    
                    if reply.startswith("chat,"):
                        chat_message = reply.split(",", 1)[1]
                        if player == 0:
                            self.car_game_states[0] = reply
                            self.clients[1].sendall(pickle.dumps({"chat": chat_message, "game_state": self.car_game_states, "enemy_car_state": self.enemy_car_state}))
                        elif player == 1:
                            self.car_game_states[1] = reply
                            self.clients[0].sendall(pickle.dumps({"chat": chat_message, "game_state": self.car_game_states, "enemy_car_state": self.enemy_car_state}))
                    for connection in self.clients:
                        connection.sendall(pickle.dumps({"game_state": reply, "enemy_car_state": self.enemy_car_state}))

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
            self.clients[0].sendall(
                pickle.dumps({"game_state": "win", "enemy_car_state": self.enemy_car_state})
            )

server = Server()
server.start()
