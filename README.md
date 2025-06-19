# 2048 Game

My implementation of the classic 2048 puzzle game using Python and Pygame.

## What it does

This is a fully playable 2048 game with a clean interface. You slide numbered tiles on a 4x4 grid to combine them and try to reach 2048. The game tracks your current score and saves your best score between sessions.

## Features

- Arrow keys or WASD controls
- Score tracking with persistent best score storage
- Color-coded tiles that change as numbers get higher
- Built-in game instructions and tips
- Restart functionality
- Proper win/lose detection

## How to run

Make sure you have Python and pygame installed:

```bash
pip install pygame
```

Then just run:

```bash
python 2048.py
```

## Controls

- Arrow keys or WASD to move tiles
- N to restart
- Q to quit
- Y/N when prompted

## Technical stuff

The game uses a 2D array to represent the board state. Movement is handled by rotating the board matrix so all moves can be processed as "move left" operations, then rotating back. 

Key files:
- `2048.py` - main game logic
- `constants.json` - colors and UI settings
- `bestscore.csv` - stores your high score

The merge algorithm handles combining tiles and the scoring system. Random tile generation places new 2s or 4s after each move.

Built with Python 3 and Pygame.
