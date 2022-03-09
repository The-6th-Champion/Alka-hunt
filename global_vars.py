from typing import Dict, List, Tuple

itemInfo: Dict[str, Tuple[str, str]] = {
    "sword": ("weapon", "A relatively weak weapon, can be used to attack most animals"),
    "hot sword": ("weapon", "A sword that's blade is hot enough to easily cauterize wounds, set fire to things, and cause a great deal of damage. It is made by forging steel sword and cinnabar together."),
    "firewood": ("material", "to be used for heating up solutions"),
    "spoon": ("material", "A very versitile utensil that is capable of being used for making Alkahest."),
    "iron shavings": ("material", "Iron shavings... could be used to make iron sulfate"),
    "sulfate": ("material", "A common item in an alchemists bag. Who knows what it can do..."),
    "Vitriol of Mars": ("component", "Also known as Ferrous sulfate, this is a component in making Alkahest. A mole of this is made with one mole of aqueous iron and one mole of sulfate"),
    "Cinnabar": ("component", "A solid substance used for making Alkahest. Found in Dragons' Lairs"),
    "bezoar": ("component", "An item found within most animals, extract using a hot sword to keep the animal alive."),
    "Dragon's Horn": ("component", "The horn of a dragon, and one of the only materials that can hold Alkahest. Must use a hot sword to cut it off."),
    "Alkahest": ("material", "The universal solvent. Congradulations, you have completed the game!")
}

animals: Dict[str, Tuple[str, int]] = {
    "goat": ("bezoar", 3, ["sword", "hot sword"]),
    "bird": ("bezoar", 1, ["sword", "hot sword"]),
    "dragon": ("bezoar", 20, ["hot sword"]),
}