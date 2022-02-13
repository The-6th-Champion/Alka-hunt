import json
from typing import List, Dict, Optional, Union, Tuple


class Inventory:
    def __init__(self, load_data: Dict) -> None:
        self.inventory = load_data["inventory"]

    def add_items(self, type: str, *, items: List[Tuple[str, int]]):
        for item in items:
            self.inventory[type][item[0]] = item[1]

def main():
    raise NotImplementedError


if __name__ == '__main__':
    player_data: Dict[str, Union[str, Dict[str, int]]
                      ] = json.load("./playerData.json")
    inventory: Inventory = Inventory(player_data)
    main()
