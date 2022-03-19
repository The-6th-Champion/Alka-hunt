from typing import List, Tuple, Optional, Dict
from control_help import Pretty
from global_vars import itemInfo, animals


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

    def save(self) -> str:
        import json
        self.player_info.position = self.area_map.player_cursor
        self.area_map.area_map[self.area_map.player_cursor[0]
                               ][self.area_map.player_cursor[1]].remove("player")
        data = {
            "player": self.player_info.player_info,
            "inventory": self.inventory.inventory,
            "achievements": {
                "all": self.achievements.all,
                "unlocked": self.achievements.unlocked
            },
            "gameover": self.gameover,
            "newGame": False,
            "area_map": self.area_map.area_map
        }
        with open(".\data\playerData.json", "w") as fpdata:
            fpdata.write(json.dumps(data, indent=4))
        self.area_map.area_map[self.area_map.player_cursor[0]
                               ][self.area_map.player_cursor[1]].append("player")
        return Pretty.success(f"Saved Successfully, {data['player']['name']}")


class AreaMap:
    def __init__(self, map_data: List[List[str]], current_position: List[str]) -> None:
        self.area_map: List[List[List[str]]] = map_data
        self.player_cursor: List[int] = current_position
        self.area_map[self.player_cursor[0]
                      ][self.player_cursor[1]].append("player")
        print(Pretty.success("Added to map!") + "\u2705")

    def move_player(self, new_pos: List[str]) -> bool:
        self.area_map[self.player_cursor[0]
                      ][self.player_cursor[1]].remove("player")
        self.player_cursor = new_pos
        self.area_map[self.player_cursor[0]
                      ][self.player_cursor[1]].append("player")
        return True

    def reveal_items(self) -> List[str]:
        items: List[str] = self.area_map[self.player_cursor[0]
                                         ][self.player_cursor[1]].copy()
        items.remove("player")
        return items


class Achievements:
    def __init__(self, achievement_data) -> None:
        self.all: List[str] = achievement_data["all"]
        self.unlocked: List[str] = achievement_data["unlocked"]
        print(Pretty.success("Achievements synced!") + "\u2705")

    def unlock(self, achievement) -> None:
        print(Pretty.success(f"Achieved: {achievement}"))
        self.unlocked.append(achievement)

    @classmethod
    def inventoryListener(self, data: PlayerData) -> None:
        if "alkahest" in data.inventory.inventory and "alkahest" not in data.achievements.unlocked:
            print(Pretty.success("CONGRADULATIONS, YOU HAVE FINISHED THE GAME!"))
            data.gameover = True
            data.achievements.unlock("Alkahest")
        if "bezoar" in data.inventory.inventory["components"] and data.inventory.inventory["components"]["bezoar"] >= 32 and "32 bezoars" not in data.achievements.unlocked:
            data.achievements.unlock("32 bezoars")
        if "Cinnabar" in data.inventory.inventory["components"] and data.inventory.inventory["components"]["Cinnabar"] >= 64 and "64g Cinnabar" not in data.achievements.unlocked:
            data.achievements.unlock("64g Cinnabar")
        if "Vitriol of Mars" in data.inventory.inventory["components"] and data.inventory.inventory["components"]["Vitriol of Mars"] >= 128 and "128mol Vitriol of Mars" not in data.achievements.unlocked:
            data.achievements.unlock("128mol Vitriol of Mars")
        if "Dragon's Horn" in data.inventory.inventory["components"] and data.inventory.inventory["components"]["Dragon's Horn"] >= 1 and "Dragon's Horn" not in data.achievements.unlocked:
            data.achievements.unlock("Dragon's Horn")
        if "spoon" in data.inventory.inventory["materials"] and data.inventory.inventory["materials"]["spoon"] <= 0 and "Its gone??" not in data.achievements.unlocked:
            print("Your spoon was vaporized!")
            data.achievements.unlock("Its gone??")

        if data.achievements.all == data.achievements.unlocked:
            print(Pretty.success("You have collected everything possible!"))
            data.achievements.unlock("Master Alchemist!")
            print(Pretty.success(
                "Made by ME for my 21-22 AP Computer Science Principles Create Task"))


class Information:
    def __init__(self, info_data) -> None:
        self.player_info = info_data
        self.name = info_data["name"]
        self.position = info_data["position"]
        print(Pretty.success("User Data synced!") + "\u2705")

    def set_position(self, pos) -> None:
        self.position = pos


class Inventory:
    def __init__(self, inventory_data: Dict) -> None:
        self.inventory: Dict[Dict[str, int]] = inventory_data
        print(Pretty.success("Inventory Loaded!") + "\u2705")

    def add_items(self, category: str, items: List[Tuple[str, int]]) -> None:
        for item in items:
            if item[0] not in self.inventory[category]:
                self.inventory[category][item[0]] = item[1]
            else:
                self.inventory[category][item[0]] += item[1]

    def view_items(self, category: Optional[str] = None) -> str:
        output: str = ""
        if category:
            output += f"{category}:\n"
            for item, count in self.inventory[category].items():
                output += f"    {item}: {count}\n"
        else:
            for cat in self.inventory:
                output += f"\t{cat}:\n"
        return output