# car_racing_client.py

from car_racing_network import Network
from car_racing import CarRacing

def run_game():
    n = Network()
    player = int(n.get_p())
    print("You are player:", player)
    
    game = CarRacing(n, player)
    game.run_car()

if __name__ == "__main__":
    run_game()
