from typing import List, Tuple, Optional, Dict
from data_vis import PlayerData
from global_vars import itemInfo, animals

class Commands:

    @classmethod
    def tbd(self, bruh=None) -> None:
        """
        Unimplemented command, check back later!
        """
        pass

    # collegeboard function
    @classmethod
    def move(self, data, directions):
        """
        Use this to move the player in the direction(s) specified.
        Usage:
            move <direction>
            move <direction> ... <direction>
            move up down right right left
        """
        player_pos: List[int] = data.area_map.player_cursor.copy()
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
        return Pretty.okay("Surroundings: " + ", ".join(data.area_map.reveal_items()))

    @classmethod
    def save(self, data: PlayerData):
        """
        Saves the current game state to a file.
        Usage:
            save
        """
        data.save()

    @classmethod
    def stop(self, data: PlayerData) -> None:
        """
        Stop the game, without erroring it :)
        Usage:
            stop
        """
        data.area_map.area_map[data.area_map.player_cursor[0]
                               ][data.area_map.player_cursor[1]].remove("player")
        exit()

    @classmethod
    def inventory(self, data: PlayerData, category: List[str] = None) -> str:
        """
        View your inventory. You can also specify a category to view.
        Usage:
            inventory
            inventory [category]
        """
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
        """
        Grab an item from the current area.
        Usage:
            grab <item>
        """
        for i in range(len(item)):
            if item[i] in data.area_map.area_map[data.area_map.player_cursor[0]][data.area_map.player_cursor[1]]:
                data.inventory.add_items(
                    category=itemInfo[item[i]][0]+"s",
                    items=[(item[i], 1)])
                data.area_map.area_map[data.area_map.player_cursor[0]
                                       ][data.area_map.player_cursor[1]].remove(item[i])
                return Pretty.success(f"{str(item).replace('[', '').replace(']', '')} added")
            else:
                return Pretty.warn(f"{str(item).replace('[', '').replace(']', '')} not found")

    @classmethod
    def help(self, data: PlayerData, command: List[str] = []) -> str:
        """
        Print out the help text for each command.
        Usage:
            help
            help [command]
        """
        all_commands: Dict[str, str] = {method: getattr(
            self, method).__doc__ for method in dir(self) if method[0] != "_"}
        if command != []:
            if command[0] in all_commands:
                return all_commands[command[0]]
            else:
                return Pretty.warn(f"Command not found: {command[0]}")
        else:
            output: str = ""
            for method in sorted(list(all_commands.keys())):
                output += Pretty.okay(f"    {method}\n")

            return f"\nCommand List:\n{output}\n{Pretty.warn('Type help <command> for more information')}"

        

    @classmethod
    def show(self, data: PlayerData) -> str:
        """
        Show the current location and surroundings of the player.
        Usage:
            show
        """
        return Pretty.okay(str(data.area_map.player_cursor) + " - " + ", ".join(data.area_map.reveal_items()))

    @classmethod
    def hunt(self, data: PlayerData, huntedAnimal: List[str]) -> str:
        """
        Hunt any present animal for its drops.
        Usage:
            hunt <animal>
        """

        for animal in huntedAnimal:
            if animal in animals and animal not in data.area_map.area_map[data.area_map.player_cursor[0]][data.area_map.player_cursor[1]]:
                return Pretty.warn(f"{animal} is not present in the area")
            elif animal in animals:
                # checks if the user has the weapons
                for weapon in animals[animal][1]:
                    if weapon not in data.inventory.inventory["weapons"]:
                        return Pretty.warn(f"You do not have {weapon}")
                    else:
                        data.inventory.add_items("components", [animals[animal]][0])
                        data.area_map.area_map[data.area_map.player_cursor[0]
                                            ][data.area_map.player_cursor[1]].remove(animal)
                        return Pretty.success(f"You have recieved {animals[animal][0][1]} {animals[animal][0][0]}{'s.' if animals[animal][0][1] > 1 else '.'}")
            else:
                return Pretty.warn("This is not a valid animal! Maybe use 'grab' instead.")

    @classmethod
    def achievements(self, data: PlayerData) -> str:
        """
        View achievements, with indication of completion.
        Usage:
            achievements
        """
        colored_achieves: List[str] = data.achievements.all.copy()
        for i, achieve in enumerate(colored_achieves):
            if achieve in data.achievements.unlocked:
                colored_achieves[i] = "\u2705 " + Pretty.success(achieve)
            else:
                colored_achieves[i] = "\u274C " + achieve
        return Pretty.okay("Achievements:") + "\n\n    " + "\n    ".join(colored_achieves)

    @classmethod
    def stove(self, data: PlayerData) -> str:
        """
        Build a stove in the current location.
        The stove is permanent and will allow you to craft items.
        Usage:
            stove
        """
        if "firewood" in data.inventory.inventory["materials"]:
            if data.inventory.inventory["materials"]["firewood"] >= 2:
                data.inventory.inventory["materials"]["firewood"] -= 2
                data.area_map.area_map[data.area_map.player_cursor[0]
                                       ][data.area_map.player_cursor[1]].append("stove")
                return Pretty.success(f"You have built a stove at this position! ({str(data.area_map.player_cursor).strip('[]')})",)
        return Pretty.warn("You need 2 firewood to make a stove!")

    @classmethod
    def craft(self, data: PlayerData, quant_args: List[str] = ["1"]) -> str:
        quantity: int = int(quant_args[0])
        """
        Craft an item.
        Usage:
            craft [item]
            craft [item] [quantity]
        """
        print(Pretty.okay(
            "What would you like to make? (type the number)\n\n    1. Alkahest\n    2. Vitriol of Mars\n    3. hot sword"))
        item = input("craft >> ")
        if item == "1":
            if ("Vitriol of Mars" in data.inventory.inventory["components"] and data.inventory.inventory["components"]["Vitriol of Mars"]) >= 128*quantity \
                    and ("Cinnabar" in data.inventory.inventory["components"] and data.inventory.inventory["components"]["Cinnabar"]) >= 64*quantity \
                    and ("bezoar" in data.inventory.inventory["components"] and data.inventory.inventory["components"]["bezoar"]) >= 32*quantity \
                    and ("Dragon's Horn" in data.inventory.inventory["components"] and data.inventory.inventory["components"]["Dragon's Horn"]) >= 1*quantity \
                    and ("spoon" in data.inventory.inventory["materials"] and data.inventory.inventory["materials"]["spoon"]) >= 1*quantity:
                data.inventory.inventory["components"]["Vitriol of Mars"] -= 128*quantity
                data.inventory.inventory["components"]["Cinnabar"] -= 64*quantity
                data.inventory.inventory["components"]["bezoar"] -= 32*quantity
                data.inventory.inventory["components"]["Dragon's Horn"] -= 1*quantity
                data.inventory.inventory["materials"]["spoon"] -= 1*quantity
                data.inventory.add_items(
                    "components", [("Alkahest", quantity)])
                return Pretty.success(f"You have crafted an Alkahest!")
            else:
                return Pretty.warn("You need a bunch of stuff to craft an Alkahest! (check achievements ;)")
        elif item == "2":
            if ("iron shavings" in data.inventory.inventory["materials"] and data.inventory.inventory["weapons"]["sword"]) >= 1*quantity \
                    and ("sulfate" in data.inventory.inventory["materials"] and data.inventory.inventory["materials"]["sulfate"]) >= 1*quantity:
                data.inventory.inventory["materials"]["iron shavings"] -= 1*quantity
                data.inventory.inventory["materials"]["sulfate"] -= 1*quantity
                data.inventory.add_items(
                    "components", [("Vitriol of Mars", quantity)])
                return Pretty.success(f"You have crafted a Vitriol of Mars!")
            else:
                return Pretty.warn("You need a 1:1 ratio of iron shavings and sulfate to craft a Vitriol of Mars!")
        elif item == "3":
            if ("sword" in data.inventory.inventory["weapons"] and data.inventory.inventory["weapons"]["sword"]) >= 1*quantity \
                    and ("Cinnabar" in data.inventory.inventory["components"] and data.inventory.inventory["components"]["Cinnabar"]) >= 3*quantity:
                data.inventory.inventory["weapons"]["sword"] -= 1*quantity
                data.inventory.inventory["components"]["Cinnabar"] -= 3*quantity
                data.inventory.add_items("weapons", [("hot sword", quantity)])
                return Pretty.success(f"You have crafted a hot sword!")

            else:
                return Pretty.warn("You need a 1:3 ratio of swords and Cinnabar to craft a hot sword!")

        else:
            return Pretty.warn("That is not a valid item!")


class Pretty:
    def warn(text) -> str:
        return "\u001b[1;93m" + text + "\u001b[0m"

    def okay(text) -> str:
        return "\u001b[1;34m" + text + "\u001b[0m"

    def success(text) -> str:
        return "\u001b[1;92m" + text + "\u001b[0m"