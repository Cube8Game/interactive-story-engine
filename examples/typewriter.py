def run(isengine):
    isengine.default_printer = isengine.TypewriterPrinter()
    inp = isengine.show_until_input("Hello! ")
    isengine.show_seconds(f"{inp}!", 3)