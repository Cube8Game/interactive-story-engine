import os

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

