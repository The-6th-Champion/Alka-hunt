from typing import List, Optional, Tuple, Dict
from global_vars import *


class PlayerData:
    def __init__(self, load_data: Dict) -> None:
        self.player_info: Information = Information(
            info_data=load_data["player"])
        self.inventory: Inventory = Inventory(
            inventory_data=load_data["inventory"])
        self.achievements: Achievements = Achievements(
            achievement_data=load_data["achievements"])
        self.gameover = load_data["gameover"]
        self.area_map: AreaMap = AreaMap(
            map_data=load_data["area_map"], current_position=load_data["player"]["position"])

    def save(self) -> Dict:
        import json
        self.player_info.position = self.area_map.player_cursor
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


class AreaMap:
    def __init__(self, map_data, current_position) -> None:
        self.area_map: List[List[str]] = map_data
        self.player_cursor = current_position
        self.area_map[self.player_cursor[0]][self.player_cursor[1]].append("player")
        print("Added to map!")

    def move_player(self, new_pos) -> None:
        self.area_map[self.player_cursor[0]][self.player_cursor[1]].remove("player")
        self.player_cursor = new_pos
        self.area_map[self.player_cursor[0]][self.player_cursor[1]].append("player")

    def reveal_items(self):
        return self.area_map[self.player_cursor[0]][self.player_cursor[1]]


class Achievements:
    def __init__(self, achievement_data) -> None:
        self.all = achievement_data["all"]
        self.unlocked = achievement_data["unlocked"]
        print("Achievements synced!")

    def unlock(self, achievement) -> None:
        self.unlocked.append(achievement)


class Information:
    def __init__(self, info_data) -> None:
        self.player_info = info_data
        self.name = info_data["name"]
        self.position = info_data["position"]
        print("User Data synced!")

    def set_position(self, pos) -> None:
        self.position = pos


class Inventory:
    def __init__(self, inventory_data: Dict) -> None:
        self.inventory = inventory_data
        print("Inventory Loaded!")

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
    def move(self, data: PlayerData, directions):
        player_pos = data.area_map.player_cursor.copy()
        if not directions:
            return "Try that again, but with a direction (up, down, left, right)"
        for direction in directions:
            if direction == "up":
                player_pos[0] -= 1
                if (player_pos[0] <= 0):
                    player_pos[0] = 0
                    print("You cannot move farther up")
            elif direction == "down":
                data.player_info.position[0] += 1
                if (data.player_info.position[0] >= 14):
                    data.player_info.position[0] = 14
                    print("You cannot move farther down")
            elif direction == "left":
                data.player_info.position[0] -= 1
                if (data.player_info.position[0] <= 0):
                    data.player_info.position[0] = 0
                    print("You cannot move farther left")
            elif direction == "right":
                data.player_info.position[0] += 1
                if (data.player_info.position[0] >= 14):
                    data.player_info.position[0] = 14
                    print("You cannot move farther right")
        data.area_map.move_player(player_pos)
        return "Surroundings: " + "".join(data.area_map.reveal_items())

    @classmethod
    def save(self, data: PlayerData):
        data.save()

    @classmethod
    def stop(self, data: PlayerData):
        self.area_map.area_map[self.player_info.position[0]][self.player_info.position[1]].remove("player")
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
        data.inventory.add_items(items[item][0], item)

    @classmethod
    def help(self, data: PlayerData):
        print("Command list")

    @classmethod
    def show(self, data: PlayerData):
        return ", ".join(data.area_map.reveal_items())

    @classmethod
    def hunt(self, data: PlayerData, animal: str):
        if animal in animals:
            data.inventory.add_items("materials", animals[animal])
            return f"You have recieved {animals[animal][1]} {animals[animal][0]}{'s.' if animals[animal][1] > 1 else '.'}"
        else:
            return "This is not a valid animal! Maybe use 'grab' instead."


class Listener:
    def inventoryListener(data: PlayerData):
        if "alkahest" in data.inventory.inventory:
            print("CONGRADULATIONS, YOU HAVE FINISHED THE GAME!")
            data.gameover = True
            data.achievements.unlock("Alkahest")
            data.save()
            print("DATA SAVED!")

    