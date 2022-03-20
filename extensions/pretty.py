
class Pretty:
    def warn(text) -> str:
        return "\u001b[1;93m" + text + "\u001b[0m"

    def okay(text) -> str:
        return "\u001b[1;34m" + text + "\u001b[0m"

    def success(text) -> str:
        return "\u001b[1;92m" + text + "\u001b[0m"
