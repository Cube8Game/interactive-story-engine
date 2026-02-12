# Interactive Story Engine

**Version:** 0.1.0  
**License:** MIT  

A Python library for creating interactive text-based story games, designed for terminal-based experiences. It provides flexible tools for rendering text, handling user input, and managing dynamic story output.

---

## Features

- **Terminal-based rendering** via `Renderer` and `TerminalRenderer`.
- **Customizable text printing** with `Printer` classes:
  - `BasicPrinter` – standard output.
  - `TypewriterPrinter` – prints text with typewriter-style animation.
  - `SkippablePrinter` – allows skipping text with a key press.
  - `ExtensionPrinter` – base class for extending printing behavior.
- **Interactive input utilities**:
  - Multiple-choice prompts.
  - Timed messages.
  - Input with optional clearing before/after display.

---

## Installation

Install via Git:

```bash
pip install git+https://gitlab.com/amysteryname/interactive-story-engine.git
````

Requires Python 3.10 or higher.

---

## Quick Start

```python
from interactive_story_engine import TerminalRenderer, BasicPrinter

# Initialize renderer and printer
renderer = TerminalRenderer()
printer = BasicPrinter(renderer)

# Clear the terminal
printer.clear()

# Display a message
printer.simple_print("Welcome to the Interactive Story Engine!\n")

# Get user input
name = printer.simple_input()
printer.simple_print(f"Hello, {name}!\n")
```

---

## Advanced Usage

### Typewriter Effect

```python
from interactive_story_engine import TypewriterPrinter

typewriter = TypewriterPrinter(printer, char_duration=0.05)
typewriter.simple_print("This text appears one character at a time...\n")
```

### Skippable Text

```python
from interactive_story_engine import SkippablePrinter

skippable = SkippablePrinter(printer)
skippable.simple_print("Press enter to skip this text...\n")
```

### Multiple Choice

```python
options = ["Go left", "Go right", "Go forward"]
choice = printer.multiple_choice("Which path will you take?", options)
printer.simple_print(f"You chose: {options[choice]}\n")
```

---

## Contributing

Contributions are welcome! Please submit a merge request or issue on the [GitLab repository](https://gitlab.com/amysteryname/interactive-story-engine).

---

## License

MIT License. See [LICENSE](https://gitlab.com/amysteryname/interactive-story-engine/-/blob/main/LICENSE) for details.


