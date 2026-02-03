import isengine

options = [
    "greeting",
    "typewriter"
]

if __name__ == "__main__":
    demo = isengine.multiple_choice("Select a demo: ", options)
    match demo:
        case 0: # greeting
            name = isengine.show_until_input("What's your name? ")
            isengine.show_seconds(f"Hi, {name}!", 3)
        case 1: # typewriter
            isengine.default_printer = isengine.TypewriterPrinter(isengine.BasicPrinter(isengine.TerminalRenderer()))
            inp = isengine.show_until_input("Hello! ")
            isengine.show_seconds(f"{inp}!", 3)