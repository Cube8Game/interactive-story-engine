import isengine

if __name__ == "__main__":
    demo = isengine.show_until_input("Select a demo: ")
    match demo:
        case "greeting":
            name = isengine.show_until_input("What's your name? ")
            isengine.show_seconds(f"Hi, {name}!", 3)
        case "typewriter":
            isengine.default_printer = isengine.TypewriterPrinter()
            inp = isengine.show_until_input("Hello! ")
            isengine.show_seconds(f"{inp}!", 3)