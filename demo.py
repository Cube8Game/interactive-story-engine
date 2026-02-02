import isengine

if __name__ == "__main__":
    name = isengine.show_until_input("What's your name? ")
    isengine.show_seconds(f"Hi, {name}!", 3)