from re import sub
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

    # def save(self) -> str:
    #     import json
    #     self.player_info.position = self.area_map.player_cursor
    #     self.area_map.area_map[self.area_map.player_cursor[0]
    #                            ][self.area_map.player_cursor[1]].remove("player")
    #     data = {
    #         "player": self.player_info.player_info,
    #         "inventory": self.inventory.inventory,
    #         "achievements": {
    #             "all": self.achievements.all,
    #             "unlocked": self.achievements.unlocked
    #         },
    #         "gameover": self.gameover,
    #         "newGame": False,
    #         "area_map": self.area_map.area_map
    #     }
    #     with open(".\data\playerData.json", "w") as fpdata:
    #         fpdata.write(json.dumps(data, indent=4))
    #     self.area_map.area_map[self.area_map.player_cursor[0]
    #                            ][self.area_map.player_cursor[1]].append("player")
    #     return f"Saved Successfully, {data['player']['name']}"


class AreaMap:
    def __init__(self, map_data: List[List[str]], current_position: List[str]) -> None:
        self.area_map: List[List[List[str]]] = map_data
        self.player_cursor: List[int] = current_position
        self.area_map[self.player_cursor[0]
                      ][self.player_cursor[1]].append("player")
        print(Pretty.perfect("Added to map!") + "\u2705")

    def move_player(self, new_pos: List[str]) -> bool:
        self.area_map[self.player_cursor[0]
                      ][self.player_cursor[1]].remove("player")
        self.player_cursor = new_pos
        self.area_map[self.player_cursor[0]
                      ][self.player_cursor[1]].append("player")
        return True

    def reveal_items(self) -> List[str]:
        items: List[str] = self.area_map[self.player_cursor[0]][self.player_cursor[1]].copy()
        items.remove("player")
        return items


class Achievements:
    def __init__(self, achievement_data) -> None:
        self.all: List[str] = achievement_data["all"]
        self.unlocked: List[str] = achievement_data["unlocked"]
        print(Pretty.perfect("Achievements synced!") + "\u2705")

    def unlock(self, achievement) -> None:
        print(Pretty.success(f"Achieved: {achievement}"))
        self.unlocked.append(achievement)

    @classmethod
    def inventoryListener(self, data: PlayerData) -> None:
        if "alkahest" in data.inventory.inventory:
            print(Pretty.perfect("CONGRADULATIONS, YOU HAVE FINISHED THE GAME!"))
            data.gameover = True
            data.achievements.unlock("Alkahest")
        print(data.inventory.inventory["components"])
        if "bezoars" in data.inventory.inventory["components"] and data.inventory.inventory["components"]["bezoars"] >= 32:
            print("yes")
            data.achievements.unlock("32 bezoars")
        if "Cinnabar" in data.inventory.inventory["components"] and data.inventory.inventory["components"]["Cinnabar"] >= 64:
            data.achievements.unlock("64g Cinnabar")
        if "Vitriol of Mars" in data.inventory.inventory["components"] and data.inventory.inventory["components"]["Vitriol of Mars"] >= 128:
            data.achievements.unlock("128mol Vitriol of Mars")
        if "Dragon's Horn" in data.inventory.inventory["components"] and data.inventory.inventory["components"]["Dragon's Horn"] >= 1:
            data.achievements.unlock("Dragon's Horn")
        if "spoon" in data.inventory.inventory["materials"] and data.inventory.inventory["materials"]["spoon"] <= 0:
            print("Your spoon was vaporized!")
            data.achievements.unlock("Its gone??")

        if data.achievements.all == data.achievements.unlocked:
            print(Pretty.perfect("You have collected everything possible!"))
            data.achievements.unlock("Master Alchemist!")
            print(Pretty.perfect("Made by ME for my 21-22 AP Computer Science Principles Create Task"))


class Information:
    def __init__(self, info_data) -> None:
        self.player_info = info_data
        self.name = info_data["name"]
        self.position = info_data["position"]
        print(Pretty.perfect("User Data synced!") + "\u2705")

    def set_position(self, pos) -> None:
        self.position = pos


class Inventory:
    def __init__(self, inventory_data: Dict) -> None:
        self.inventory: Dict[Dict[str,int]] = inventory_data
        print(Pretty.perfect("Inventory Loaded!") + "\u2705")

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


class Commands:

    @classmethod
    def tbd(self, bruh = None) -> None:
        pass

    # collegeboard function
    @classmethod
    def move(self, data, directions):
        player_pos = data.area_map.player_cursor.copy()
        if not directions:
            return Pretty.warn("Try that again, but with a direction (up, down, left, right)")
        for direction in directions:
            if direction == "up":
                player_pos[0] -= 1
                if (player_pos[0] <= 0):
                    player_pos[0] = 0
                    print(Pretty.warn("You cannot move farther up"))
            elif direction == "down":
                player_pos[0] += 1
                if (player_pos[0] >= 14):
                    player_pos[0] = 14
                    print(Pretty.warn("You cannot move farther down"))
            elif direction == "left":
                player_pos[1] -= 1
                if (player_pos[1] <= 0):
                    player_pos[1] = 0
                    print(Pretty.warn("You cannot move farther left"))
            elif direction == "right":
                player_pos[1] += 1
                if (player_pos[1] >= 14):
                    player_pos[1] = 14
                    print(Pretty.warn("You cannot move farther right"))
        data.area_map.move_player(player_pos)
        return "Surroundings: " + ", ".join(data.area_map.reveal_items())

    # @classmethod
    # def save(self, data: PlayerData):
    #     data.save()

    @classmethod
    def stop(self, data: PlayerData) -> None:
        data.area_map.area_map[data.area_map.player_cursor[0]
                               ][data.area_map.player_cursor[1]].remove("player")
        exit()

    @classmethod
    def inventory(self, data: PlayerData, category: List[str] = None) -> str:
        output: str = ""
        if not category:
            categories: str = data.inventory.view_items()
            print("Choose a category:\n", categories)
            cat = input("Category >> ")
            output += data.inventory.view_items(cat)
        else:
            output += data.inventory.view_items(category[0])
        return output

    @classmethod
    def grab(self, data: PlayerData, item: List[str]) -> str:
        for i in range(len(item)):
            if item[i] in data.area_map.area_map[data.area_map.player_cursor[0]][data.area_map.player_cursor[1]]:
                data.inventory.add_items(
                    category=itemInfo[item[i]][0]+"s", 
                    items=[(item[i], 1)])
                data.area_map.area_map[data.area_map.player_cursor[0]][data.area_map.player_cursor[1]].remove(item[i])
        return f"{str(item).replace('[', '').replace(']', '')} added"

    @classmethod
    def help(self, data: PlayerData) -> str:
        
        cmd_list: List[str] = [

        ]
        return f"Command List:\n\n"+'\n'.join(cmd_list)
        

    @classmethod
    def show(self, data: PlayerData) -> str:
        return str(data.area_map.player_cursor) + " - " + ", ".join(data.area_map.reveal_items())

    @classmethod
    def hunt(self, data: PlayerData, huntedAnimal: str) -> str:
        for animal in huntedAnimal:
            if animal in animals and animal not in data.area_map.area_map[data.area_map.player_cursor[0]][data.area_map.player_cursor[1]]:
                return Pretty.warn(f"{animal} is not present in the area")
            elif animal in animals:
                data.inventory.add_items("components", [animals[animal]])
                data.area_map.area_map[data.area_map.player_cursor[0]][data.area_map.player_cursor[1]].remove(animal)
                return Pretty.success(f"You have recieved {animals[animal][1]} {animals[animal][0]}{'s.' if animals[animal][1] > 1 else '.'}")
            else:
                return Pretty.warn("This is not a valid animal! Maybe use 'grab' instead.")

    @classmethod
    def achievements(self, data: PlayerData) -> str:
        colored_achieves: List[str] = data.achievements.all.copy()
        for i, achieve in enumerate(colored_achieves):
            if achieve in data.achievements.unlocked:
                colored_achieves[i] = Pretty.perfect(achieve)
        return Pretty.okay("Achievements:") + "\n\n    " + "\n    ".join(colored_achieves)

class Pretty:
    def warn(text) -> str:
        return "\u001b[1;93m" + text + "\u001b[0m"

    def success(text) -> str:
        return "\u001b[1;96m" + text + "\u001b[0m"

    def okay(text) -> str:
        return "\u001b[1;34m" + text + "\u001b[0m"
        
    def perfect(text) -> str:
        return "\u001b[1;92m" + text + "\u001b[0m"