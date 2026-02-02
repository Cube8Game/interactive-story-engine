import os
import time

def clear() -> None: # Only supports Linux for now
    os.system("clear")

def show_until_input(message: str, clear_start: bool = True, clear_end: bool = True) -> str:
    inp = ""
    if clear_start:
        clear()
    try:
        inp = input(message)
    except KeyboardInterrupt:
        raise
    finally:
        if clear_end:
            clear()
    return inp

def show_seconds(message: str, duration, clear_start: bool = True, clear_end: bool = True):
    if clear_start:
        clear()
    try:
        print(message, end="", flush=True)
        time.sleep(duration)
    except KeyboardInterrupt:
        raise
    finally:
        if clear_end:
            clear()
