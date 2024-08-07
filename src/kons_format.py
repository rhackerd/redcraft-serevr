from colorama import Fore, Back, Style


class consoleFormat:
    def __init__(self, text):
        self.text = text
        self.print_list = ""
        self.color_list = {
            "black": Fore.BLACK,
            "red": Fore.RED,
            "green": Fore.GREEN,
            "yellow": Fore.YELLOW,
            "blue": Fore.BLUE,
            "magenta": Fore.MAGENTA,
            "cyan": Fore.CYAN,
            "white": Fore.WHITE,
            "bright black": Fore.LIGHTBLACK_EX,
            "bright red": Fore.LIGHTRED_EX,
            "bright green": Fore.LIGHTGREEN_EX,
            "bright yellow": Fore.LIGHTYELLOW_EX,
            "bright blue": Fore.LIGHTBLUE_EX,
            "bright magenta": Fore.LIGHTMAGENTA_EX,
            "bright cyan": Fore.LIGHTCYAN_EX,
            "bright white": Fore.LIGHTWHITE_EX,
        }
        self.background_color_list = {
            "bg_black": Back.BLACK,
            "bg_red": Back.RED,
            "bg_green": Back.GREEN,
            "bg_yellow": Back.YELLOW,
            "bg_blue": Back.BLUE,
            "bg_magenta": Back.MAGENTA,
            "bg_cyan": Back.CYAN,
            "bg_white": Back.WHITE,
            "bg_bright_black": Back.LIGHTBLACK_EX,
            "bg_bright_red": Back.LIGHTRED_EX,
            "bg_bright_green": Back.LIGHTGREEN_EX,
            "bg_bright_yellow": Back.LIGHTYELLOW_EX,
            "bg_bright_blue": Back.LIGHTBLUE_EX,
            "bg_bright_magenta": Back.LIGHTMAGENTA_EX,
            "bg_bright_cyan": Back.LIGHTCYAN_EX,
            "bg_bright_white": Back.LIGHTWHITE_EX,
        }

    def setText(self, value):
        self.text = value

    def format(self):
        self.print_list = "" # reset the print list (resets just the output text for next usage)
        checkNext = False # variable for checking if next char is > 
        nextCharIsValue = False # variable for searching &
        ActColor = "silver"
        nextBold = False
        nextDim = False
        stop = False
        text = ""

        for char in self.text:
            if char == "&":
                nextCharIsValue = True
            elif nextCharIsValue:
                if char == "<":
                    ActColor = ""
                    checkNext = True
                elif char == ">" and checkNext == True:
                    try:
                        text += self.color_list[ActColor]
                    except KeyError:
                        text += self.color_list["white"]
                    checkNext = False
                    nextCharIsValue = False
                else:
                    if checkNext:
                            ActColor += char
                    else:
                        if char == "l":
                            text += Style.BRIGHT

                        elif char == "r":
                            text += Style.RESET_ALL

                        elif char == "d":
                            text += Style.DIM
                        nextCharIsValue = False
            else:
                text += char


        return text






if __name__ == "__main__":
    test = consoleFormat("test&<red>&rtest")
    print(test.format())