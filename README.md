
# Installation

```
python3 -m venv .venv
source .venv/bin/activate
pip3 install pygame-ce
```

# Run

```
python3 main.py <scene>
```

## Scenes

### bullet

Simple bullet flight mechanic.
To shoot a bullet click, drag and release.
Bullet will fly in a direction of your movement.

### tower

press B to build tower. 
Click to choose position.
ESC to cancel build.

When not in build mode, click to start shooting.

### path

simple monster spawn and path finding logic

TODO:
* for better testing, need to add building towers, to create mazes
* rounds since we recalc paths on each round start

