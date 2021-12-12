# py-GameUI

A Python package to use GUI Widgets like Button, Textinput & Slider in pygame.

Install using:
```shell
pip install py-GameUI
```

# Documentation
You could check out the docs at https://aman333nolawz.github.io/py-GameUI/

# Usage

```python
import pygame

import py_GameUI

W, H = 600, 600
screen = pygame.display.set_mode((W, H))

elements = [
    py_GameUI.Button(
        [10, 10, 100, 100],
        text="Hello world",
        function=lambda: print("You clicked on the button"),
    ),
    py_GameUI.Input_box([10, 150, 150, 20]),
    py_GameUI.Slider(10, 210, 10, 30),
]

while True:
    screen.fill("#1c1c1c")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        for element in elements:
            element.events(event)

    for element in elements:
        element.draw(screen)
    pygame.display.flip()

```
