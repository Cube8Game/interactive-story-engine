import time
import uuid
import typing
from abc import ABC, abstractmethod
from .renderer import Renderer

class Printer(ABC):
    def __init__(self, renderer: Renderer):
        self.renderer: Renderer = renderer

    @abstractmethod
    def simple_print(self, message: str, force_immediate: bool = False, stop_condition: typing.Callable|None = None):
        pass

    @abstractmethod
    def simple_input(self) -> str:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    def show_until_input(self, message: str, clear_start: bool = True, clear_end: bool = True) -> str:
        inp: str = ""
        if clear_start:
            self.clear()
        try:
            self.simple_print(message)
            inp = self.simple_input()
        finally:
            if clear_end:
                self.clear()
        return inp
    
    def show_seconds(self, message: str, duration: float, clear_start: bool = True, clear_end: bool = True) -> None:
        if clear_start:
            self.clear()
        try:
            self.simple_print(message)
            time.sleep(duration)
        finally:
            if clear_end:
                self.clear()
    
    def multiple_choice(self, message: str, options: list[str], number_delimiter: str = ") ", minimum_index: int = 1, clear_start: bool = True, clear_end: bool = True):
        inp: str = ""
        while not (len(inp) > 0 and (inp.isdigit() or inp in options)):
            if clear_start:
                self.clear()
            try:
                actual_message = message + "\n"
                for i, option in enumerate(options):
                    actual_message += str(i + minimum_index) + number_delimiter + option + "\n"
                self.simple_print(actual_message)
                inp = self.simple_input()
            finally:
                if clear_end:
                    self.clear()
        if inp.isdigit():
            return int(inp) - minimum_index
        else:
            return options.index(inp)

class ExtensionPrinter(Printer):
    def __init__(self, parent: Printer):
        self.parent: Printer = parent
        super().__init__(self.parent.renderer)


class BasicPrinter(Printer):
    def simple_print(self, message: str, force_immediate: bool = False, stop_condition: typing.Callable|None = None):
        self.renderer.write(message)
    
    def simple_input(self) -> str:
        return self.renderer.read()
    
    def clear(self) -> None: 
        self.renderer.clear()

class TypewriterPrinter(ExtensionPrinter):
    def __init__(self, parent: Printer, char_duration: float = 0.1):
        super().__init__(parent)
        self.char_duration: float = char_duration

    def simple_print(self, message: str, force_immediate: bool = False, stop_condition: typing.Callable|None = None):
        if force_immediate:
            self.parent.simple_print(message, True)
            return True
        return_false: typing.Callable = lambda: False
        actual_stop_condition: typing.Callable = stop_condition or return_false
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
    def simple_print(self, message: str, force_immediate: bool = False, stop_condition: typing.Callable|None = None):
        my_uuid = uuid.uuid4()
        skip: typing.Callable = lambda: my_uuid if self.renderer.submitted() else None
        actual_stop_condition: typing.Callable = skip
        if stop_condition:
            actual_stop_condition = lambda: stop_condition() or skip()
        skipped = self.parent.simple_print(message, force_immediate, actual_stop_condition)
        if skipped is not None:
            if skipped == my_uuid:
                self.parent.clear()
                self.parent.simple_print(message, True)
            else:
                return skipped

    def simple_input(self) -> str:
        return self.parent.simple_input()
    
    def clear(self) -> None:
        self.parent.clear()