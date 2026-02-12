import os
import sys
import select

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

    @abstractmethod
    def submitted(self) -> bool:
        pass

class TerminalRenderer(Renderer):
    def read(self) -> str:
        return input()
    
    def write(self, message: str) -> None:
        print(message, end="", flush=True)
    
    def clear(self) -> None: # Only supports Unix systems for now
        os.system("clear")
    
    def submitted(self):
        if select.select([sys.stdin], [], [], 0)[0]:
            sys.stdin.read(1)
            return True
        return False
