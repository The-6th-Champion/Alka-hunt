import json
from typing import List, Dict, Optional, Union, Tuple


class PlayerData:
    def __init__(self, load_data: Dict) -> None:
        self.player_info: Information = Information(
            info_data=load_data["player"])
        self.inventory: Inventory = Inventory(
            inventory_data=load_data["inventory"])
        self.achievements: Achievements = Achievements(
            achievement_data=load_data["achievements"])
        self.gameover = load_data["gameover"]

    def save(self) -> Dict:
        raise NotImplementedError


class Achievements:
    def __init__(self, achievement_data) -> None:
        self.all = achievement_data["all"]
        self.unlocked = achievement_data["unlocked"]

    def unlock(self, achievement) -> None:
        self.unlocked.append(achievement)


class Information:
    def __init__(self, info_data) -> None:
        self.player_info = info_data
        self.name = info_data["name"]
        self.position = info_data["position"]

    def set_position(self, pos) -> None:
        self.position = pos


class Inventory:
    def __init__(self, inventory_data: Dict) -> None:
        self.inventory = inventory_data

    def add_items(self, type: str, *, items: List[Tuple[str, int]]):
        for item in items:
            self.inventory[type][item[0]] = item[1]

    def view_items(self, category: str = None) -> List[str]:
        output: str = ""
        if category:
            output += f"{category}:\n"
            for item, count in self.inventory[category].items():
                output += f"    {item}: {count}\n"
        else:
            for cat in self.inventory:
                output += f"{cat}:\n"
                for item, count in self.inventory[cat].items():
                    output += f"    {item}: {count}\n"
        return output


def main(player_data: PlayerData):
    raise NotImplementedError


if __name__ == '__main__':
    raw_player_data: Dict[str, Union[str, Dict[str, int]]
                          ] = json.load("./playerData.json")
    player_data: PlayerData = PlayerData(raw_player_data)
    main(player_data)
