import json
from typing import List, Dict, Optional, Union, Tuple, Callable
import os
from helper_classes import *
from global_vars import items

commands: Dict[str, Callable] = {
    "save": Commands.save,
    "stop": Commands.stop,
    "inventory": Commands.inventory,
    "grab": Commands.grab,
    "move": Commands.move,
    "help": Commands.help,
    "show": Commands.show
}

#  AP CREATE FUNCTION
def game(player_data: PlayerData) -> None:
    # Game loop
    while True:
        prompt = input(">> ").strip().split(" ")
        if not prompt:
            continue
        if prompt[0] in commands and len(prompt) > 1:
            print(commands[prompt[0]](player_data, prompt[1:]))
            pass
        elif prompt[0] in commands and len(prompt) == 1:
            print(commands[prompt[0]](data=player_data))
        else:
            print("this is not a command. use the 'help' command for a list of commands.")

        Achievements.inventoryListener(player_data)


if __name__ == '__main__':
    with open("./data/playerData.json", "r") as fpdata:
        raw_player_data: Dict[str, Union[str, Dict[str, int]]
                              ] = json.load(fpdata)
    if raw_player_data["newGame"] == True:
        raw_player_data["player"]["name"] = input("Enter player name >> ")
    print(f'Welcome to Alka-hassle, {raw_player_data["player"]["name"]}!')
    player_data: PlayerData = PlayerData(raw_player_data)
    game(player_data)
