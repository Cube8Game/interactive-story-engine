def run(isengine):
    name = isengine.show_until_input("What's your name? ")
    isengine.show_seconds(f"Hi, {name}!", 3)