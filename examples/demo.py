import interactive_story_engine as ise
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
    ise.BasicPrinter(ise.TerminalRenderer()),
    ise.SkippablePrinter(ise.TypewriterPrinter(ise.BasicPrinter(ise.TerminalRenderer())))
]

default_printer = printers[0]

def set_default_printer(new_printer):
    default_printer = new_printer
    bossfight.default_printer = new_printer

if __name__ == "__main__":

    while True:
        choice = default_printer.multiple_choice("Select an option", menu)
        match choice:
            case 0: # Run demo
                bossfight.bossfight("Skeleton Warrior", 60, bossfight.Weapon("Sword", 10, 10, 0.3, 3.0))
            case 1: # Change printer
                default_printer = printers[default_printer.multiple_choice("Select a printer", printer_select)]
                bossfight.default_printer = default_printer
            case 2: # Quit
                break