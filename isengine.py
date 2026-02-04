import os
import time
import sys
import select
import uuid

from abc import ABC, abstractmethod


class Renderer(ABC):
    @abstractmethod
    def read(self) -> str:
        pass

    @abstractmethod
    def write(self, message: str) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
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
    def simple_print(self, message: str, force_immediate: bool = False, stop_condition: callable|None = None):
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
    def simple_print(self, message: str, force_immediate: bool = False, stop_condition: callable|None = None):
        self.renderer.write(message)
    
    def simple_input(self) -> str:
        return self.renderer.read()
    
    def clear(self) -> None: 
        self.renderer.clear()

class TypewriterPrinter(ExtensionPrinter):
    def __init__(self, parent: Printer, char_duration: float = 0.1):
        super().__init__(parent)
        self.char_duration: float = char_duration

    def simple_print(self, message: str, force_immediate: bool = False, stop_condition: callable|None = None):
        if force_immediate:
            self.parent.simple_print(message, True)
            return True
        return_false: callable = lambda: False
        actual_stop_condition: callable = stop_condition or return_false
        for c in message:
            self.parent.simple_print(c, force_immediate, actual_stop_condition)
            time.sleep(self.char_duration)
            stop = stop_condition()
            if stop is not None:
                return stop

    def simple_input(self) -> str:
        return self.parent.simple_input()
    
    def clear(self) -> None:
        self.parent.clear()

class SkippablePrinter(ExtensionPrinter):
    def simple_print(self, message: str, force_immediate: bool = False, stop_condition: callable|None = None):
        my_uuid = uuid.uuid4()
        skip: callable = lambda: my_uuid if select.select([sys.stdin], [], [], 0)[0] else None
        actual_stop_condition: callable = skip
        if stop_condition:
            actual_stop_condition = lambda: stop_condition() or skip()
        skipped = self.parent.simple_print(message, force_immediate, actual_stop_condition)
        if skipped is not None:
            if skipped == my_uuid:
                sys.stdin.read(1)
                self.parent.clear()
                self.parent.simple_print(message, True)
            else:
                return skipped

    def simple_input(self) -> str:
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
            actual_message = message + "\n"
            for i, option in enumerate(options):
                actual_message += str(i + minimum_index) + number_delimiter + option + "\n"
            actual_printer.simple_print(actual_message)
            inp = actual_printer.simple_input()
        finally:
            if clear_end:
                actual_printer.clear()
    if inp.isdigit():
        return int(inp) - minimum_index
    else:
        return options.index(inp)