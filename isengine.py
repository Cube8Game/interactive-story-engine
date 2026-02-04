import os
import time

from abc import ABC, abstractmethod


class Renderer(ABC):
    @abstractmethod
    def read(self) -> str:
        pass

    @abstractmethod
    def write(self, message: str) -> None:
        pass

    @abstractmethod
    def clear(self):
        pass

class TerminalRenderer(Renderer):
    def read(self) -> str:
        return input()
    
    def write(self, message: str) -> None:
        print(message, end="", flush=True)
    
    def clear(self) -> None: # Only supports Unix systems for now
        os.system("clear")


class Printer(ABC):
    def __init__(self, renderer: Renderer):
        self.renderer: Renderer = renderer

    @abstractmethod
    def simple_print(self, message: str) -> None:
        pass

    @abstractmethod
    def simple_input(self) -> str:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

class ExtensionPrinter(Printer):
    def __init__(self, parent: Printer):
        self.parent: Printer = parent
        super().__init__(self.parent.renderer)


class BasicPrinter(Printer):
    def simple_print(self, message: str) -> None:
        self.renderer.write(message)
    
    def simple_input(self) -> str:
        return self.renderer.read()
    
    def clear(self) -> None: 
        self.renderer.clear()

class TypewriterPrinter(ExtensionPrinter):
    def __init__(self, parent: Printer, char_duration: float = 0.1):
        super().__init__(parent)
        self.char_duration: float = char_duration

    def simple_print(self, message: str) -> None:
        for c in message:
            self.parent.simple_print(c)
            time.sleep(self.char_duration)

    def simple_input(self):
        return self.parent.simple_input()
    
    def clear(self) -> None:
        self.parent.clear()


default_printer = BasicPrinter(TerminalRenderer())


def show_until_input(message: str, clear_start: bool = True, clear_end: bool = True, printer: Printer|None = None) -> str:
    actual_printer: Printer = printer or default_printer
    inp: str = ""
    if clear_start:
        actual_printer.clear()
    try:
        actual_printer.simple_print(message)
        inp = actual_printer.simple_input()
    finally:
        if clear_end:
            actual_printer.clear()
    return inp

def show_seconds(message: str, duration: float, clear_start: bool = True, clear_end: bool = True, printer: Printer|None = None) -> None:
    actual_printer: Printer = printer or default_printer
    if clear_start:
        actual_printer.clear()
    try:
        actual_printer.simple_print(message)
        time.sleep(duration)
    finally:
        if clear_end:
            actual_printer.clear()

def multiple_choice(message: str, options: list[str], number_delimiter: str = ") ", minimum_index: int = 1, clear_start: bool = True, clear_end: bool = True, printer: Printer|None = None):
    actual_printer: Printer = printer or default_printer
    inp: str = ""
    while not (len(inp) > 0 and (inp.isdigit() or inp in options)):
        if clear_start:
            actual_printer.clear()
        try:
            actual_printer.simple_print(message + "\n")
            for i, option in enumerate(options):
                actual_printer.simple_print(str(i + minimum_index) + number_delimiter + option + "\n")
            inp = actual_printer.simple_input()
        finally:
            if clear_end:
                actual_printer.clear()
    if inp.isdigit():
        return int(inp) - minimum_index
    else:
        return options.index(inp)