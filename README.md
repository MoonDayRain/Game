# Blackjack Game (Pygame)

## Overview
This project is a Blackjack game developed using Python and the Pygame library.
In addition to standard Blackjack rules, the game introduces multiple **Dealer Modes**
that alter dealer behavior to create unique and challenging gameplay.

The project demonstrates modular programming, object-oriented design,
and algorithmic decision-making.

---

## Features
- Classic Blackjack rules
- Multiple Dealer Modes:
  - Normal
  - Heaven (special bonus condition)
  - Rigged (probability manipulation)
  - Impossible (dealer forces exact 21)
  - Beginner
- Betting system with balance tracking
- Win and round statistics
- Graphical interface using Pygame

---

## Dependencies
- Python 3.x
- Pygame

Install dependencies using:
```bash
pip install pygame
```

---

## How to Run
1. Ensure Python 3 is installed.
2. Install required dependencies.
3. Run the game using:
```bash
python main.py
```

---

## Project Structure
- main.py — Main game loop
- config.py — Game configuration and constants
- game_state.py — Global game state
- cards.py — Card and deck logic
- round_logic.py — Game round and scoring logic
- input_handler.py — Input handling
- draw.py — Rendering logic
- buttons.py — UI components
- screens.py — Start and lose screens

---

## AI Usage Declaration
AI tools were used for documentation support and code structure review.
All final logic and implementation decisions were made by me.
