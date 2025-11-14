# Dungeon Escape

A thrilling terminal-based dungeon crawler adventure game written in Python!

## Description

Navigate through a dangerous dungeon filled with monsters, treasures, and deadly traps. Fight various enemies, collect gold and items, manage your health, and ultimately face the Ancient Dragon in an epic final battle!

## Features

- **Turn-based Combat System**: Fight goblins, orcs, skeletons, dark knights, and a dragon boss
- **Character Progression**: Improve your attack and defense through treasure finds
- **Inventory Management**: Collect gold, potions, and powerful items
- **Multiple Room Types**: Combat encounters, treasure rooms, and mysterious empty chambers
- **Colorful ASCII Interface**: Vibrant terminal colors for an immersive experience
- **Dynamic Gameplay**: Random encounters and events keep each playthrough unique
- **Health Management**: Strategic use of potions and rest periods
- **Boss Battle**: Epic final showdown with an Ancient Dragon

## How to Play

### Installation & Running

```bash
# Make the file executable
chmod +x dungeon_escape.py

# Run the game
python3 dungeon_escape.py
```

### Gameplay

1. **Explore**: Venture deeper into the dungeon to find treasures and enemies
2. **Fight**: Engage in turn-based combat with various monsters
3. **Survive**: Manage your health with potions and strategic resting
4. **Collect**: Gather gold and items to become stronger
5. **Conquer**: Defeat the Ancient Dragon to win!

### Combat Actions

- **Attack**: Deal damage to the enemy
- **Defend**: Reduce incoming damage on the next enemy attack
- **Use Potion**: Restore 40 HP (limited supply)
- **Flee**: Attempt to escape from battle (40% success rate)

### Tips

- Don't waste potions early - save them for tough fights
- Defending can save your life against strong enemies
- Explore thoroughly to find upgrades and gold
- Rest carefully - you might get ambushed!
- The Dragon appears in room 5 - be prepared!

## Requirements

- Python 3.6 or higher
- Terminal with ANSI color support (most modern terminals)

## Game Mechanics

- **Health**: Starts at 100 HP, use potions and rest to recover
- **Attack**: Base 15 damage, can be increased with weapon finds
- **Defense**: Base 5, reduces incoming damage
- **Potions**: Start with 3, can find more during exploration
- **Gold**: Earned by defeating enemies and finding treasures

## Enemies

- **Goblin**: Weak but numerous (30 HP, 8 ATK)
- **Skeleton**: Undead warrior (35 HP, 10 ATK)
- **Orc**: Brutish fighter (50 HP, 12 ATK)
- **Dark Knight**: Heavily armored foe (70 HP, 18 ATK)
- **Ancient Dragon**: Final boss (150 HP, 25 ATK)

## License

Free to play and modify! Have fun escaping the dungeon!

## Credits

Created with Python and passion for classic dungeon crawlers!
