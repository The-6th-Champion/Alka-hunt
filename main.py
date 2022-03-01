from typing import List, Dict, Optional, Union, Tuple, Callable
from helper_classes import *
from global_vars import itemInfo

commands: Dict[str, Callable] = {
    "save": Commands.tbd,
    "stop": Commands.stop,
    "inventory": Commands.inventory,
    "grab": Commands.grab,
    "move": Commands.move,
    "help": Commands.help,
    "show": Commands.show,
    "hunt": Commands.hunt,
    "achievements": Commands.achievements,
}

def game(player_data: PlayerData) -> None:
    # Game loop
    while True:
        prompt: List[str] = input("\n>> ").strip().split(" ")
        if not prompt:
            continue
        if prompt[0] in commands and len(prompt) > 1:
            print(commands[prompt[0]](player_data, prompt[1:]))
            pass
        elif prompt[0] in commands and len(prompt) == 1:
            print(commands[prompt[0]](data=player_data))
        else:
            print("this is not a command. use the 'help' command for a list of commands.")
            print ("hi")

        Achievements.inventoryListener(player_data)


if __name__ == '__main__':
    raw_player_data: Dict[str, Union[str, Dict[str, int]]
                              ] = {
  "player": {
    "name": "",
    "position": [0, 0]
  },
  "inventory": {
    "materials": {
      "spoon": 1,
      "sulfate": 128
    },
    "weapons": {},
    "components": {}
  },
  "achievements": {
    "all": [
      "32 bezoars",
      "64g Cinnabar",
      "128mol Vitriol of Mars",
      "Dragon's Horn",
      "Its gone??",
      "Alkahest"
    ],
    "unlocked": []
  },
  "gameover": False,
  "newGame": True,
  "area_map": [
    [
      ["goat", "goat", "sword"],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      []
    ],
    [[], [], [], [], [], [], [], [], [], [], [], [], [], [], []],
    [
      ["firewood"],
      ["firewood"],
      ["firewood"],
      ["firewood"],
      ["firewood"],
      ["firewood"],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      []
    ],
    [
      ["firewood"],
      ["firewood"],
      ["firewood"],
      ["firewood"],
      ["firewood"],
      ["firewood"],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      []
    ],
    [
      ["firewood"],
      ["firewood"],
      ["firewood"],
      ["firewood"],
      ["firewood"],
      ["firewood"],
      [],
      [],
      [],
      [],
      [],
      ["goat", "goat"],
      ["goat", "goat"],
      [],
      []
    ],
    [
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      ["bird", "goat"],
      ["goat", "goat"],
      [],
      ["bird"],
      [],
      []
    ],
    [
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      ["bird", "goat"],
      ["goat", "goat"],
      [],
      [],
      [],
      []
    ],
    [
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      ["bird", "goat"],
      ["goat", "goat"],
      [],
      [],
      [],
      []
    ],
    [
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      ["bird", "goat"],
      ["goat", "goat"],
      [],
      [],
      [],
      []
    ],
    [[], [], [], [], [], [], [], [], [], [], [], [], [], [], []],
    [[], [], [], [], [], [], [], [], [], [], [], [], [], [], []],
    [
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      ["dragon", "Cinnabar", "Cinnabar"],
      ["Cinnabar", "Cinnabar", "Cinnabar"],
      ["Cinnabar", "Cinnabar", "Cinnabar"],
      ["Cinnabar", "Cinnabar", "Cinnabar"],
      ["Cinnabar", "Cinnabar", "Cinnabar"]
    ],
    [
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      ["Cinnabar", "Cinnabar", "Cinnabar"],
      ["Cinnabar", "Cinnabar", "Cinnabar"],
      ["Cinnabar", "Cinnabar", "Cinnabar"]
    ],
    [
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      ["bird", "Cinnabar", "Cinnabar", "Cinnabar"],
      ["Cinnabar", "Cinnabar", "Cinnabar"],
      ["Cinnabar", "Cinnabar", "Cinnabar"]
    ],
    [
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      ["Cinnabar", "Cinnabar", "Cinnabar"],
      ["Cinnabar", "Cinnabar", "Cinnabar"]
    ]
  ]
}

    if raw_player_data["newGame"] == True:
        raw_player_data["player"]["name"] = input("Enter player name >> ")
    print(f'Welcome to Alka-hunt, {raw_player_data["player"]["name"]}!')
    player_data: PlayerData = PlayerData(raw_player_data)
    game(player_data)
