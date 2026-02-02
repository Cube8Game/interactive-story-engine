import os
import time

from abc import ABC, abstractmethod


class Printer(ABC):
    @abstractmethod
    def simple_print(self, message: str) -> None:
        pass

    @abstractmethod
    def simple_input(self) -> str:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

class TerminalPrinter(Printer):
    def simple_print(self, message: str) -> None:
        print(message, end="", flush=True)
    
    def simple_input(self) -> str:
        return input()
    
    def clear(self) -> None: # Only supports Unix systems for now
        os.system("clear")

class TypewriterPrinter(TerminalPrinter):
    def simple_print(self, message: str, char_duration: float = 0.1) -> None:
        for c in message:
            print(c, end="", flush=True)
            time.sleep(char_duration)


default_printer = TerminalPrinter()


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

def show_seconds(message: str, duration, clear_start: bool = True, clear_end: bool = True, printer: Printer|None = None) -> None:
    actual_printer: Printer = printer or default_printer
    if clear_start:
        actual_printer.clear()
    try:
        actual_printer.simple_print(message)
        time.sleep(duration)
    finally:
        if clear_end:
            actual_printer.clear()
