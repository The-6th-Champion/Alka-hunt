import json
from typing import List, Dict, Optional, Union, Tuple, Callable
import os
from helper_classes import *

commands: Dict[str, Callable] = {
    "save": Commands.save,
    "stop": Commands.stop,
    "inventory": Commands.inventory,
    "grab": Commands.grab,
    "move": Commands.tbd,
    "help": Commands.help,
}

items: Dict[str, Tuple[str, str]] = {
    "steal sword": ("weapon", "A relatively weak weapon, can be used to attack most animals"),
    "hot sword": ("weapon", "A sword that's blade is hot enough to easily cauterize wounds, set fire to things, and cause a great deal of damage. It is made by forging steel sword and cinnabar together."),
    "firewood": ("material", "to be used for heating up solutions"),
    "spoon": ("material", "A very versitile utensil that is capable of being used for making Alkahest."),
    "iron shavings": ("material", "Iron shavings... could be used to make iron sulfate"),
    "sulfate": ("material", "A common item in an alchemists bag. Who knows what it can do..."),
    "Vitriol of Mars": ("component", "Also known as Ferrous sulfate, this is a component in making Alkahest. A mole of this is made with one mole of aqueous iron and one mole of sulfate"),
    "Cinnabar": ("component", "A solid substance used for making Alkahest. Found in Dragons' Lairs"),
    "bezoar": ("component", "An item found within most animals, extract using a hot sword to keep the animal alive."),
    "Dragon's Horn": ("component", "The horn of a dragon, and one of the only materials that can hold Alkahest. Must use a hot sword to cut it off."),
}


def main(player_data: PlayerData) -> None:
    # Game loop
    while True:
        prompt = input(">> ").strip().split(" ")
        if not prompt:
            continue
        if prompt[0] in commands and len(prompt) > 1:
            print(commands[prompt[0]](player_data, **prompt[2:]))
            pass
        elif prompt[0] in commands and len(prompt) == 1:
            print(commands[prompt[0]](data=player_data))
        else:
            print("this is not a command. use the 'help' command for a list of commands.")


if __name__ == '__main__':
    with open("./playerData.json", "r") as fpdata:
        raw_player_data: Dict[str, Union[str, Dict[str, int]]
                              ] = json.load(fpdata)
    if raw_player_data["newGame"] == True:
        raw_player_data["player"]["name"] = input("Enter player name >> ")
    print(f'Welcome to Alka-hassle, {raw_player_data["player"]["name"]}!')
    player_data: PlayerData = PlayerData(raw_player_data)
    main(player_data)
