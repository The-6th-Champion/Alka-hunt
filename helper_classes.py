from typing import List, Optional, Tuple, Dict

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

    def view_items(self, category: Optional[str] = None) -> List[str]:
        output: str = ""
        if category:
            output += f"{category}:\n"
            for item, count in self.inventory[category].items():
                output += f"    {item}: {count}\n"
        else:
            for cat in self.inventory:
                output += f"{cat}:\n"
        return output


class Commands:

    @classmethod
    def tbd() -> None:
        pass

    @classmethod
    def save(data: PlayerData):
        data.save()

    @classmethod
    def stop(data: PlayerData):
        exit()

    @classmethod
    def inventory(data: PlayerData):
        output: str = ""
        categories: str = data.inventory.view_items()
        print("Choose a category:\n", categories)
        cat = input("Category >> ")
        output += data.inventory.view_items(cat)
        return output
    
    @classmethod
    def grab(data: PlayerData, item: Tuple[str, int]):
        data.inventory.add_items()
    
    @classmethod
    def help(data: PlayerData):
        print("Command list")