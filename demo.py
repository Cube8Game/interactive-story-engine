import isengine
import bossfight

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
    isengine.SkippablePrinter(isengine.TypewriterPrinter(isengine.BasicPrinter(isengine.TerminalRenderer())))
]

if __name__ == "__main__":
    while True:
        choice = isengine.multiple_choice("Select an option", menu)
        match choice:
            case 0: # Run demo
                bossfight.bossfight("Skeleton Warrior", 60, bossfight.Weapon("Sword", 10, 10, 0.3, 3.0))
            case 1: # Change printer
                isengine.default_printer = printers[isengine.multiple_choice("Select a printer", printer_select)]
            case 2: # Quit
                break