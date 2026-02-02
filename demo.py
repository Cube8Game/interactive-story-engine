from examples import greeting, typewriter
import isengine

if __name__ == "__main__":
    demo = isengine.show_until_input("Select a demo: ")
    match demo:
        case "greeting":
            greeting.run(isengine)
        case "typewriter":
            typewriter.run(isengine)