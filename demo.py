import isengine

menu = [
    "Run demo",
    "Change printer",
    "Quit"
]

printer_select = [
    "Basic printer",
    "Typewriter"
]

printers = [
    isengine.BasicPrinter(isengine.TerminalRenderer()),
    isengine.TypewriterPrinter(isengine.BasicPrinter(isengine.TerminalRenderer()))
]

if __name__ == "__main__":
    while True:
        choice = isengine.multiple_choice("Select an option", menu)
        match choice:
            case 0: # Run demo
                name = isengine.show_until_input("What's your name? ")
                isengine.show_seconds(f"Hi, {name}!", 3)
            case 1: # Change printer
                isengine.default_printer = printers[isengine.multiple_choice("Select a printer", printer_select)]
            case 2: # Quit
                break