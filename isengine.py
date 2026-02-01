import os

def clear(): # Only supports Linux for now
    os.system("clear")

def show_until_input(message, clear_start=True, clear_end=True):
    if clear_start:
        clear()
    try:
        input(message)
    except KeyboardInterrupt:
        raise
    finally:
        if clear_end:
            clear()

