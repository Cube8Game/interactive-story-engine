import isengine
import random

class Item:
    def __init__(self, name: str):
        self.name = name

class Weapon(Item):
    def __init__(self, name: str, base_damage: int, max_bonus: int, crit_chance: float, crit_multiplier: float):
        super().__init__(name)
        self.base_damage = base_damage
        self.max_bonus = max_bonus
        self.crit_chance = crit_chance
        self.crit_multiplier = crit_multiplier

    def get_damage(self) -> int:
        damage = self.base_damage
        damage += random.randint(0, self.max_bonus)
        if random.random() < self.crit_chance:
            damage = int(damage * self.crit_multiplier)
        return damage

class Food(Item):
    def __init__(self, name: str, base_regen: int, max_bonus: int):
        super().__init__(name)
        self.base_regen = base_regen
        self.max_bonus = max_bonus
    
    def get_regen(self):
        return self.base_regen + random.randint(0, self.max_bonus)

menu = [
    "Run demo",
    "Change printer",
    "Quit"
]

printer_select = [
    "Basic printer",
    "Typewriter"
]

printers = [
    isengine.BasicPrinter(isengine.TerminalRenderer()),
    isengine.SkippablePrinter(isengine.TypewriterPrinter(isengine.BasicPrinter(isengine.TerminalRenderer())))
]

inventory = [
    Weapon("Hammer", 20, 10, 0.2, 1.5),
    Food("Pie", 100, 0),
    Food("Apple", 15, 5),
    Food("Apple", 15, 5),
    Food("Apple", 15, 5),
    Food("Apple", 15, 5),
    Food("Apple", 15, 5),
    Food("Apple", 15, 5),
    Food("Apple", 15, 5),
    Food("Apple", 15, 5)
]

fight_menu = [
    "Inventory",
    "Flee"
]

def bossfight(boss_name: str, boss_max_health: int, boss_weapon: Weapon):
    boss_health = boss_max_health
    player_max_health = 100
    player_health = player_max_health
    menu_prompt = f"{boss_name} approaches!"
    while True:
        choice = isengine.multiple_choice(menu_prompt, fight_menu)
        match choice:
            case 0:
                choice = isengine.multiple_choice("Select an item to use", map(lambda x: x.name, inventory))
                item = inventory[choice]
                if isinstance(item, Food):
                    regen = item.get_regen()
                    player_health += regen
                    player_health = min(player_health, player_max_health)
                    isengine.show_seconds(f"You ate the {item.name} and gained {regen} HP! You now have {player_health} HP.", 3)
                elif isinstance(item, Weapon):
                    damage = item.get_damage()
                    boss_health -= damage
                    boss_health = max(boss_health, 0)
                    isengine.show_seconds(f"You hit {boss_name} and dealt {damage} damage! {boss_name} now has {boss_health} HP.", 3)
                    if boss_health <= 0:
                        isengine.show_seconds(f"{boss_name} collapsed!", 2)
                        break
            case 1:
                isengine.show_seconds("You flee the scene...", 2)
                break
        damage = boss_weapon.get_damage()
        player_health -= damage
        menu_prompt = f"{boss_name} hit you with the {boss_weapon.name} and dealt {damage} damage! You now have {player_health} HP."

if __name__ == "__main__":
    while True:
        choice = isengine.multiple_choice("Select an option", menu)
        match choice:
            case 0: # Run demo
                bossfight("Skeleton Warrior", 60, Weapon("Sword", 10, 10, 0.3, 3.0))
            case 1: # Change printer
                isengine.default_printer = printers[isengine.multiple_choice("Select a printer", printer_select)]
            case 2: # Quit
                break