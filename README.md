# 2024-Autumn-Pygame
2024 (Autumn) Pygame workshop SOLUTION and SPEC, blanks will go on a new branch later on

## Setup
You need to make sure you have `python3` and `pygame` installed.

### Python
Install `python3` with the installer or package manager of your choice, pip (python package manager) will come installed by default.

Check that python3 is installed: 
```
$ python3
Python 3.11.7
```

### Pygame
Install the pygame module using `pip3 install pygame` / `pip install pygame` (should be installed globally by default, but if you have a venv set up you will have to make sure it is installed in the venv)

To check that you've successfully installed pygame run the following commands (or you could just try running the program):
```
$ python3

Python 3.11.7 ...
Type "help", "copyright", "credits" or "license" for more information.

>>> import pygame

pygame 2.5.2 (SDL 2.28.3, Python 3.11.7)
Hello from the pygame community. https://www.pygame.org/contribute.html
```

## Running the Program
You can either click the `Run` button on vscode, or 
```
$ cd 2024-Autumn-Pygame
$ python ./main.py
```

## What goes where
Feel free to move around/change/add/remove files! The files are somewhat grouped up but i'm not 100% sure if the layout is intuitive

- `main.py` - Where the game is initialised and program is run, might be a good idea to abstract away as much functionality into separate files/functions if possible
- `spec/` - For now, if you want to write up some documentation for your code just create a new `.md` file and dump your notes. We will also put the cleaned up and properly fomatted spec there. Any images in the spec should be in the `spec/images/` folder
- `sprites/` - Assets for the game, for development purposes i have created some placeholder sprites that have collision boxes outlined to make life easier in `sprites/temp/`. plsplspls make sure we are using proper sprites for the actual workshop
- `src/` - code in general should go here
    - general constants can go in `src/constants.py`
    - classes/objects/tiles in `src/entities/`
    - maybe an intro or ending scene asw in `src/scenes/` ? maybe maps in here idk


## Things to note
- tile size is 64px * 64px
- board size is 10 x 14 tiles
- player movement should be setup, player's get_x() and get_y() return their center position, otherwise coordinates will be the top left corner (not tested)
