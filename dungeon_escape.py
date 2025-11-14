#!/usr/bin/env python3
"""
Dungeon Escape - A Terminal Adventure Game
Navigate through a dangerous dungeon, fight monsters, collect treasures, and defeat the Dragon!
"""

import random
import sys
import os
import time


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'


class Player:
    """Player character with stats and inventory"""

    def __init__(self, name):
        self.name = name
        self.max_hp = 100
        self.hp = 100
        self.attack = 15
        self.defense = 5
        self.gold = 0
        self.inventory = []
        self.potions = 3

    def take_damage(self, damage):
        """Apply damage to player with defense calculation"""
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        return actual_damage

    def heal(self, amount):
        """Heal player"""
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp

    def use_potion(self):
        """Use a health potion"""
        if self.potions > 0:
            self.potions -= 1
            healed = self.heal(40)
            return healed
        return 0

    def is_alive(self):
        """Check if player is still alive"""
        return self.hp > 0

    def display_stats(self):
        """Display player statistics"""
        health_bar = self._get_health_bar()
        print(f"\n{Colors.CYAN}{'='*50}{Colors.END}")
        print(f"{Colors.BOLD}{self.name}'s Status:{Colors.END}")
        print(f"{Colors.GREEN}HP: {health_bar} {self.hp}/{self.max_hp}{Colors.END}")
        print(f"{Colors.YELLOW}Attack: {self.attack} | Defense: {self.defense}{Colors.END}")
        print(f"{Colors.MAGENTA}Gold: {self.gold} | Potions: {self.potions}{Colors.END}")
        if self.inventory:
            print(f"{Colors.BLUE}Inventory: {', '.join(self.inventory)}{Colors.END}")
        print(f"{Colors.CYAN}{'='*50}{Colors.END}\n")

    def _get_health_bar(self):
        """Generate visual health bar"""
        bar_length = 20
        filled = int((self.hp / self.max_hp) * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)
        return f"[{bar}]"


class Enemy:
    """Enemy with stats and combat abilities"""

    def __init__(self, name, hp, attack, defense, gold, description):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.gold = gold
        self.description = description

    def take_damage(self, damage):
        """Apply damage to enemy"""
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        return actual_damage

    def is_alive(self):
        """Check if enemy is still alive"""
        return self.hp > 0

    def get_attack_damage(self):
        """Calculate enemy attack damage with randomness"""
        return random.randint(self.attack - 3, self.attack + 3)


class Game:
    """Main game controller"""

    ENEMIES = {
        'goblin': ('Goblin', 30, 8, 2, 15, "A small, green creature with sharp teeth"),
        'orc': ('Orc', 50, 12, 4, 25, "A brutish warrior with a massive club"),
        'skeleton': ('Skeleton', 35, 10, 3, 20, "An undead warrior rattling with each step"),
        'dark_knight': ('Dark Knight', 70, 18, 8, 50, "A corrupted knight in black armor"),
        'dragon': ('Ancient Dragon', 150, 25, 10, 200, "A massive dragon with scales like obsidian")
    }

    def __init__(self):
        self.player = None
        self.current_room = 0
        self.rooms_cleared = 0
        self.game_over = False

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')

    def slow_print(self, text, delay=0.03):
        """Print text with typewriter effect"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def display_banner(self):
        """Display game banner"""
        banner = f"""
{Colors.RED}╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        {Colors.BOLD}DUNGEON ESCAPE{Colors.END}{Colors.RED}                                  ║
║                                                           ║
║        {Colors.YELLOW}⚔️  Fight Monsters  💰 Collect Treasure{Colors.END}{Colors.RED}        ║
║        {Colors.YELLOW}🗝️  Explore Rooms   🐉 Defeat the Dragon{Colors.END}{Colors.RED}      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝{Colors.END}
"""
        print(banner)
        print(f"\n{Colors.CYAN}Welcome, brave adventurer!{Colors.END}")
        ...
        ...

    def start_game(self):
        """Initialize and start the game"""
        self.clear_screen()
        self.display_banner()

        print(f"\n{Colors.CYAN}Welcome, brave adventurer!{Colors.END}")
        name = input(f"\n{Colors.YELLOW}What is your name? {Colors.END}").strip()

        if not name:
            name = "Hero"

        self.player = Player(name)
        self.clear_screen()

        self.slow_print(f"\n{Colors.GREEN}Welcome, {self.player.name}!{Colors.END}")
        self.slow_print(f"{Colors.WHITE}You wake up in a dark, damp dungeon...{Colors.END}")
        self.slow_print(f"{Colors.WHITE}The air is thick with danger. You must escape!{Colors.END}")

        input(f"\n{Colors.CYAN}Press Enter to begin your adventure...{Colors.END}")

        self.game_loop()

    def game_loop(self):
        """Main game loop"""
        while not self.game_over and self.player.is_alive():
            self.clear_screen()
            self.player.display_stats()

            choice = self.display_room_options()

            if choice == '1':
                self.explore_room()
            elif choice == '2':
                self.rest()
            elif choice == '3':
                self.check_inventory()
            elif choice == '4':
                if self.confirm_quit():
                    self.game_over = True
                    print(f"\n{Colors.YELLOW}You fled the dungeon... Perhaps another day.{Colors.END}")
            else:
                print(f"{Colors.RED}Invalid choice!{Colors.END}")
                time.sleep(1)

        if not self.player.is_alive():
            self.game_over_screen(victory=False)
        elif not self.game_over:
            self.game_over_screen(victory=True)

    def display_room_options(self):
        """Display available actions"""
        print(f"{Colors.BOLD}What will you do?{Colors.END}")
        print(f"{Colors.GREEN}1.{Colors.END} Explore deeper into the dungeon")
        print(f"{Colors.GREEN}2.{Colors.END} Rest and recover")
        print(f"{Colors.GREEN}3.{Colors.END} Check inventory")
        print(f"{Colors.GREEN}4.{Colors.END} Flee the dungeon (quit)")

        return input(f"\n{Colors.YELLOW}Enter your choice (1-4): {Colors.END}").strip()

    def explore_room(self):
        """Explore a new room"""
        self.current_room += 1

        print(f"\n{Colors.CYAN}You venture deeper into the dungeon...{Colors.END}")
        time.sleep(1.5)

        # Boss fight at room 5
        if self.current_room == 5:
            self.boss_fight()
            return

        # Random encounter
        encounter_type = random.choice(['combat', 'combat', 'treasure', 'empty'])

        if encounter_type == 'combat':
            self.combat_encounter()
        elif encounter_type == 'treasure':
            self.treasure_encounter()
        else:
            self.empty_room()

    def combat_encounter(self):
        """Handle combat encounter"""
        # Choose enemy based on progression
        if self.current_room <= 2:
            enemy_type = random.choice(['goblin', 'skeleton'])
        else:
            enemy_type = random.choice(['goblin', 'orc', 'skeleton', 'dark_knight'])

        enemy_data = self.ENEMIES[enemy_type]
        enemy = Enemy(*enemy_data)

        print(f"\n{Colors.RED}⚔️  A {enemy.name} appears!{Colors.END}")
        print(f"{Colors.WHITE}{enemy.description}{Colors.END}")
        time.sleep(1)

        self.battle(enemy)

    def battle(self, enemy):
        """Combat system"""
        print(f"\n{Colors.RED}{'='*50}")
        print(f"BATTLE: {self.player.name} vs {enemy.name}")
        print(f"{'='*50}{Colors.END}\n")

        while enemy.is_alive() and self.player.is_alive():
            print(f"\n{Colors.YELLOW}Enemy HP: {enemy.hp}/{enemy.max_hp}{Colors.END}")
            print(f"{Colors.GREEN}Your HP: {self.player.hp}/{self.player.max_hp}{Colors.END}")

            print(f"\n{Colors.BOLD}Your turn:{Colors.END}")
            print(f"{Colors.GREEN}1.{Colors.END} Attack")
            print(f"{Colors.GREEN}2.{Colors.END} Defend (reduce damage next turn)")
            print(f"{Colors.GREEN}3.{Colors.END} Use Potion ({self.player.potions} remaining)")
            print(f"{Colors.GREEN}4.{Colors.END} Try to flee")

            choice = input(f"\n{Colors.YELLOW}Choose action (1-4): {Colors.END}").strip()

            defending = False

            if choice == '1':
                damage = random.randint(self.player.attack - 3, self.player.attack + 5)
                actual_damage = enemy.take_damage(damage)
                print(f"\n{Colors.GREEN}You strike for {actual_damage} damage!{Colors.END}")
                time.sleep(1)

            elif choice == '2':
                print(f"\n{Colors.BLUE}You brace yourself for the enemy's attack!{Colors.END}")
                defending = True
                time.sleep(1)

            elif choice == '3':
                healed = self.player.use_potion()
                if healed > 0:
                    print(f"\n{Colors.GREEN}You drink a potion and recover {healed} HP!{Colors.END}")
                else:
                    print(f"\n{Colors.RED}You have no potions left!{Colors.END}")
                time.sleep(1)

            elif choice == '4':
                if random.random() < 0.4:
                    print(f"\n{Colors.YELLOW}You successfully fled from battle!{Colors.END}")
                    time.sleep(1.5)
                    return
                else:
                    print(f"\n{Colors.RED}You failed to escape!{Colors.END}")
                    time.sleep(1)
            else:
                print(f"{Colors.RED}Invalid choice! You hesitate...{Colors.END}")
                time.sleep(1)

            # Enemy turn
            if enemy.is_alive():
                enemy_damage = enemy.get_attack_damage()
                if defending:
                    enemy_damage = max(1, enemy_damage // 2)
                    print(f"\n{Colors.BLUE}You block some of the attack!{Colors.END}")

                actual_damage = self.player.take_damage(enemy_damage)
                print(f"{Colors.RED}The {enemy.name} attacks for {actual_damage} damage!{Colors.END}")
                time.sleep(1.5)

        if not self.player.is_alive():
            return

        # Victory
        print(f"\n{Colors.GREEN}{'='*50}")
        print(f"VICTORY! You defeated the {enemy.name}!")
        print(f"{'='*50}{Colors.END}")
        print(f"{Colors.YELLOW}You gained {enemy.gold} gold!{Colors.END}")

        self.player.gold += enemy.gold
        self.rooms_cleared += 1

        # Random potion drop
        if random.random() < 0.3:
            self.player.potions += 1
            print(f"{Colors.GREEN}You found a health potion!{Colors.END}")

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

    def boss_fight(self):
        """Final boss battle"""
        print(f"\n{Colors.RED}{'='*60}")
        print(f"{Colors.BOLD}You enter a massive chamber...{Colors.END}")
        print(f"{'='*60}{Colors.END}\n")

        self.slow_print(f"{Colors.RED}A deafening roar shakes the walls!{Colors.END}")
        self.slow_print(f"{Colors.RED}The Ancient Dragon awakens!{Colors.END}")

        input(f"\n{Colors.YELLOW}Press Enter to face your destiny...{Colors.END}")

        dragon = Enemy(*self.ENEMIES['dragon'])
        self.battle(dragon)

        if self.player.is_alive():
            self.victory_screen()

    def treasure_encounter(self):
        """Find treasure"""
        treasures = [
            ("a chest of gold coins", 30, None),
            ("a gleaming sword", 15, 'attack'),
            ("a sturdy shield", 10, 'defense'),
            ("a pile of gold", 25, None),
            ("2 health potions", 0, 'potions')
        ]

        treasure = random.choice(treasures)
        name, gold, bonus = treasure

        print(f"\n{Colors.YELLOW}💰 You found {name}!{Colors.END}")

        if gold > 0:
            self.player.gold += gold
            print(f"{Colors.GREEN}+{gold} gold{Colors.END}")

        if bonus == 'attack':
            self.player.attack += 3
            print(f"{Colors.GREEN}Your attack increased by 3!{Colors.END}")
        elif bonus == 'defense':
            self.player.defense += 2
            print(f"{Colors.GREEN}Your defense increased by 2!{Colors.END}")
        elif bonus == 'potions':
            self.player.potions += 2
            print(f"{Colors.GREEN}You gained 2 health potions!{Colors.END}")

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

    def empty_room(self):
        """Empty room encounter"""
        messages = [
            "The room is empty, but you feel watched...",
            "Nothing here but dust and cobwebs.",
            "You find old bones scattered on the floor.",
            "The walls are covered in ancient runes.",
            "A cold breeze sends shivers down your spine."
        ]

        print(f"\n{Colors.WHITE}{random.choice(messages)}{Colors.END}")
        time.sleep(2)

    def rest(self):
        """Rest to recover health"""
        print(f"\n{Colors.CYAN}You take a moment to rest...{Colors.END}")

        if random.random() < 0.3:
            print(f"{Colors.RED}You were ambushed while resting!{Colors.END}")
            time.sleep(1)
            self.combat_encounter()
        else:
            healed = self.player.heal(20)
            print(f"{Colors.GREEN}You recover {healed} HP.{Colors.END}")
            time.sleep(2)

    def check_inventory(self):
        """Display inventory"""
        self.clear_screen()
        print(f"\n{Colors.CYAN}{'='*50}")
        print(f"INVENTORY")
        print(f"{'='*50}{Colors.END}\n")

        print(f"{Colors.YELLOW}Gold: {self.player.gold}{Colors.END}")
        print(f"{Colors.GREEN}Health Potions: {self.player.potions}{Colors.END}")
        print(f"{Colors.MAGENTA}Rooms Cleared: {self.rooms_cleared}{Colors.END}")

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

    def confirm_quit(self):
        """Confirm player wants to quit"""
        choice = input(f"\n{Colors.RED}Are you sure you want to quit? (yes/no): {Colors.END}").strip().lower()
        return choice in ['yes', 'y']

    def victory_screen(self):
        """Display victory message"""
        self.clear_screen()
        victory_banner = f"""
{Colors.GREEN}╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║                    {Colors.BOLD}VICTORY!{Colors.END}{Colors.GREEN}                              ║
║                                                           ║
║        You have defeated the Ancient Dragon!             ║
║        The dungeon is yours!                             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝{Colors.END}
"""
        print(victory_banner)
        print(f"\n{Colors.YELLOW}Final Stats:{Colors.END}")
        print(f"{Colors.GREEN}Rooms Cleared: {self.rooms_cleared}{Colors.END}")
        print(f"{Colors.YELLOW}Gold Collected: {self.player.gold}{Colors.END}")
        print(f"{Colors.MAGENTA}HP Remaining: {self.player.hp}/{self.player.max_hp}{Colors.END}")

        self.game_over = True

    def game_over_screen(self, victory):
        """Display game over message"""
        self.clear_screen()

        if not victory:
            game_over_banner = f"""
{Colors.RED}╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║                   GAME OVER                               ║
║                                                           ║
║        You have fallen in the dungeon...                 ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝{Colors.END}
"""
            print(game_over_banner)
            print(f"\n{Colors.YELLOW}You defeated {self.rooms_cleared} rooms{Colors.END}")
            print(f"{Colors.YELLOW}You collected {self.player.gold} gold{Colors.END}")

        print(f"\n{Colors.CYAN}Thanks for playing!{Colors.END}")


def main():
    """Main entry point"""
    try:
        game = Game()
        game.start_game()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Game interrupted. Goodbye!{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}An error occurred: {e}{Colors.END}")


if __name__ == "__main__":
    main()
