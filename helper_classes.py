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
        import json
        data = {
            "player": self.player_info.player_info,
            "inventory": self.inventory.inventory,
            "achievements": {
                "all": self.achievements.all, 
                "unlocked": self.achievements.unlocked
                },
            "gameover": self.gameover,
            "newGame": False
            }
        print(data)
        with open(".\playerData.json", "w") as fpdata:
            fpdata.write(json.dumps(data, indent=4))
        return f"Saved Successfully, {data['player']['name']}"


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

    def add_items(self, category: str, *, items: List[Tuple[str, int]]):
        for item in items:
            if item[0] not in self.inventory[category]:
                self.inventory[category][item[0]] = item[1]
            else:
                self.inventory[category][item[0]] += item[1]
                

    def view_items(self, category: Optional[str] = None) -> List[str]:
        output: str = ""
        if category:
            output += f"{category}:\n"
            for item, count in self.inventory[category].items():
                output += f"    {item}: {count}\n"
        else:
            for cat in self.inventory:
                output += f"\t{cat}:\n"
        return output


class Commands:

    @classmethod
    def tbd(self) -> None:
        pass

    @classmethod
    def save(self, data: PlayerData):
        data.save()

    @classmethod
    def stop(self, data: PlayerData):
        exit()

    @classmethod
    def inventory(self, data: PlayerData):
        output: str = ""
        categories: str = data.inventory.view_items()
        print("Choose a category:\n", categories)
        cat = input("Category >> ")
        output += data.inventory.view_items(cat)
        return output
    
    @classmethod
    def grab(self, data: PlayerData, item: Tuple[str, int]):
        data.inventory.add_items()
    
    @classmethod
    def help(self, data: PlayerData):
        print("Command list")