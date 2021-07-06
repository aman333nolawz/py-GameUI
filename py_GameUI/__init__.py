"""
A Simple module for making GUIs in pygame.
You can make Buttons, Input Boxes, Sliders and gradient rectangle with this module.
"""
from typing import Union

import pygame

vec = pygame.math.Vector2

pygame.init()


class Button:
    def __init__(
        self,
        relative_rect: pygame.Rect,
        enabled: bool = True,
        text: str = "",
        image: pygame.Surface = None,
        image_x: int = 0,
        image_y: int = 0,
        bg: Union[tuple, pygame.Color] = (124, 124, 124),
        fg: Union[tuple, pygame.Color] = (255, 255, 255),
        cc: Union[tuple, pygame.Color] = (13, 80, 213),
        hc: Union[tuple, pygame.Color] = (160, 160, 160),
        border: int = 2,
        border_color: Union[tuple, pygame.Color] = (0, 0, 0),
        border_radius: Union[int, tuple, list] = (0, 0, 0, 0),
        font: pygame.font.Font = pygame.font.SysFont("arial", 25),
        ipadx: int = 0,
        ipady: int = 0,
        function=None,
    ):
        """Initializing the button
        :param relative_rect: The coordinates and the size of the button
        :param enabled: If you want the button to be whether enabled or disabled. Default to True
        :param text: The text you want to display in the button
        :param image: The image you want to blit
        :param image_x: X Coordinate of the image
        :param image_y: Y Coordinate of the image
        :param bg: The background color of the button
        :param fg: Color of the font
        :param cc: Color of the button when clicked
        :param hc: Color of the button when hovered
        :param border: The width of the border you want
        :param border_color: Color of the border of the Button
        :param border_radius: Border radius for the button
        :param font: Name of the font you want to display the text
        :type font: class`pygame.font.Font`
        :param ipadx: The internal x-padding of the button
        :param ipady: The internal y-padding of the button
        :param function: The function you want to call when the button is pressed
        """
        # Coordinates and logics
        self.rect = relative_rect
        self.x = self.rect.x
        self.y = self.rect.y
        self.width = self.rect.width
        self.height = self.rect.height
        self.pos = vec(self.x, self.y)
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((0, 0, 0))
        self.surface.set_colorkey((0, 0, 0))
        self.enabled = enabled
        self.function = function
        self.hovered = False
        self.clicked = False

        # Colors
        self.bg = bg
        self.fg = fg
        self.hc = hc
        self.cc = cc

        if isinstance(border_radius, int):
            self.border_radius = [
                border_radius,
                border_radius,
                border_radius,
                border_radius,
            ]
        elif isinstance(border_radius, tuple):
            self.border_radius = [
                border_radius[0],
                border_radius[1],
                border_radius[2],
                border_radius[3],
            ]
        self.border_color = border_color
        self.border = border

        # Font
        self.text = text
        self.font = font
        self.ipadx = ipadx
        self.ipady = ipady

        # Image
        self.image = image
        self.image_x = image_x
        self.image_y = image_y

    def draw(self, win):
        """Draws the button to the screen
        :param win: The surface to draw the button to
        :type win: class:`pygame.Surface`
        """
        # Drawing the border around the Button
        # and for showing color keyed black colors in surface black color
        pygame.draw.rect(
            win,
            (0, 0, 0),
            (self.x, self.y, self.width, self.height),
            0,
            *self.border_radius,
        )
        pygame.draw.rect(
            win,
            self.border_color,
            (
                self.x - self.border,
                self.y - self.border,
                self.width + self.border * 2,
                self.height + self.border * 2,
            ),
            0,
            *self.border_radius,
        )

        if self.clicked:
            pygame.draw.rect(
                self.surface,
                self.cc,
                (0, 0, self.width, self.height),
                0,
                *self.border_radius,
            )
        elif self.hovered:
            pygame.draw.rect(
                self.surface,
                self.hc,
                (0, 0, self.width, self.height),
                0,
                *self.border_radius,
            )
        else:
            pygame.draw.rect(
                self.surface,
                self.bg,
                (0, 0, self.width, self.height),
                0,
                *self.border_radius,
            )

        if len(self.text) > 0:
            self.show_text()

        if self.image:
            self.surface.blit(self.image, (self.image_x, self.image_y))
        win.blit(self.surface, self.pos)

    def show_text(self):
        """Blits the the text into screen"""
        font = self.font
        text = font.render(self.text, False, self.fg)
        size = text.get_size()
        x, y = (self.width // 2 - (size[0] // 2)) + self.ipadx, (self.height // 2 - (size[1] // 2)) + self.ipady
        pos = vec(x, y)
        self.surface.blit(text, pos)

    def events(self, event):
        """Function to handle all the events with the button like clicking, hovering etc.
        :param event: The event object to look for
        :type event: class:`pygame.event.Event`
        """
        pos = pygame.mouse.get_pos()
        if (pos[0] > self.pos[0]) and (pos[0] < self.pos[0] + self.width):
            if (pos[1] > self.pos[1]) and (pos[1] < self.pos[1] + self.height):
                if self.enabled:
                    self.hovered = True

            else:
                self.hovered = False
        else:
            self.hovered = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()

            if (position[0] > self.pos[0]) and (position[0] < self.pos[0] + self.width):  # noqa: E501
                if (position[1] > self.pos[1]) and (position[1] < self.pos[1] + self.height):  # noqa: E501
                    if self.enabled:
                        self.clicked = True

                        if self.function:
                            self.function()

        if event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False


class Input_box:
    def __init__(
        self,
        relative_rect: pygame.Rect,
        bg_color=(124, 124, 124),
        active_color=(255, 255, 255),
        font_size=18,
        fg=(0, 0, 0),
        border=0,
        border_color=(0, 0, 0),
    ):

        # Coords and logics
        self.rect = relative_rect
        self.x = self.rect.x
        self.y = self.rect.y
        self.width = self.rect.width
        self.height = self.rect.height
        self.pos = vec(self.x, self.y)
        self.surface = pygame.Surface((self.width, self.height))
        self.active = False

        # Colors
        self.bg_color = bg_color
        self.active_color = active_color
        self.border_color = border_color
        self.fg = fg

        # Fonts
        self.text = ""
        self.text_size = font_size
        self.font = pygame.font.SysFont("Times New Roman", self.text_size)

        self.border = border

    def draw(self, window):
        """Draws the input box to the screen
        :param win: The surface to draw the button to
        :type win: class:`pygame.Surface`
        """
        if not self.active:
            if self.border == 0:
                self.surface.fill(self.bg_color)
            else:
                self.surface.fill(self.border_color)
                pygame.draw.rect(
                    self.surface,
                    self.bg_color,
                    (
                        self.border,
                        self.border,
                        self.width - self.border * 2,
                        self.height - self.border * 2,
                    ),
                )
        else:
            if self.border == 0:
                self.surface.fill(self.active_color)
            else:
                self.surface.fill(self.border_color)
                pygame.draw.rect(
                    self.surface,
                    self.active_color,
                    (
                        self.border,
                        self.border,
                        self.width - self.border * 2,
                        self.height - self.border * 2,
                    ),
                )

        text = self.font.render(self.text, False, self.fg)

        # getting the height and width of text
        text_height = text.get_height()
        text_width = text.get_width()

        # drawing text into screen
        if not self.active:
            self.surface.blit(text, (self.border * 2, (self.height - text_height) // 2))
        else:
            if text_width < self.width - self.border * 2:
                self.surface.blit(text, (self.border * 2, (self.height - text_height) // 2))
            else:
                self.surface.blit(
                    text,
                    (
                        (self.border * 2) + (self.width - text_width - self.border * 3),  # noqa: E501
                        (self.height - text_height) // 2,
                    ),
                )

        window.blit(self.surface, self.pos)

    def events(self, event):
        """A function to handle all the events
        :param event: The event object to look for
        :type event: class:`pygame.event.Event`
        """
        # Checks click in box
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[0] > self.x and pos[0] < self.x + self.width:
                if pos[1] > self.y and pos[1] < self.y + self.height:
                    self.active = True

                else:
                    self.active = False

            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif str((event.unicode).encode()).find("\\") == -1:
                    self.text += event.unicode


class Slider:
    def __init__(
        self,
        x: int,
        y: int,
        from_: int = 0,
        to_: int = 3,
        part_size: int = 10,
        bg: tuple = (54, 54, 54),
        cc: tuple = (13, 80, 213),
        hc: tuple = (160, 160, 160),
        fg: tuple = (255, 255, 255),
        thumb_bg: tuple = (124, 124, 124),
        font_family: str = "arial",
        font_size: int = 16,
        show_numbers: bool = True,
    ):
        """A Slider GUI for pygame.
        params:
            x:The X position of the slider
            y:The Y position of the slider
            from_: Where The value starts from
            to_: Where the value ends
            part_size: The size for one part in the slider
            bg: Background color of the Slider
            cc: Color when the thumb is clicked
            hc: Color when the thumb is hovered
            fg: Color of the font to be displayed
            thumb_bg: Background color of the thumb
            font_family: The font family of the number displayed (Font should be a system font)
            font_size: The font size of the number displayed
            show_numbers: True if you want the numbers to be shown
        """

        self.x = x
        self.y = y
        self.pos = vec(x, y)
        self.from_ = from_
        self.to_ = to_
        self.width = to_ * part_size
        self.height = 25
        self.surface = pygame.Surface((self.width, self.height))
        self.active = False
        self.hovering = False

        thumb_width = self.width // (to_ - (from_ - 1))
        self.thumb = pygame.Rect(0, 0, thumb_width, self.height)

        self.bg = bg
        self.hc = hc
        self.cc = cc
        self.thumb_bg = thumb_bg
        self.fg = fg

        self.font = pygame.font.SysFont(font_family, font_size)

        self.value = (self.from_ - 1) + ((self.thumb.x + self.thumb.w) / self.thumb.w)
        self.show_numbers = show_numbers

    def draw(self, window):
        """A function that draws the slider into the  pygame screen
        :param window: The window to draw the slider to
        :type window: class:`pygame.Surface`
        """

        self.value = (self.from_ - 1) + ((self.thumb.x + self.thumb.w) / self.thumb.w)
        self.surface.fill(self.bg)

        if self.active:
            pygame.draw.rect(self.surface, self.cc, self.thumb)
        elif self.hovering:
            pygame.draw.rect(self.surface, self.hc, self.thumb)
        else:
            pygame.draw.rect(self.surface, self.thumb_bg, self.thumb)

        if self.show_numbers:
            text_from = self.font.render(str(self.from_), True, (255, 255, 255))
            x_from, y_from = self.x, self.y + self.height + 5
            from_pos = vec(x_from, y_from)
            window.blit(text_from, from_pos)

            text_to = self.font.render(str(self.to_), True, (255, 255, 255))
            width = text_to.get_width()
            x_to = self.x + (self.width - width)
            y_to = self.y + self.height + 5
            to_pos = vec(x_to, y_to)
            window.blit(text_to, to_pos)

        window.blit(self.surface, self.pos)

    def events(self, event):
        """A function to handle all events like clicking, moving, hovering and more
        :param event: The event object to look for
        :type event: class:`pygame.event.Event`
        """

        pos = pygame.mouse.get_pos()

        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                inside_pos = self.x - pos[0]
                if (abs(inside_pos) > self.thumb.x) and (abs(inside_pos) < self.thumb.x + self.thumb.w):
                    self.hovering = True

                else:
                    self.hovering = False
            else:
                self.hovering = False
        else:
            self.hovering = False

        if self.active:
            inside_pos = self.x - pos[0]

            # Checks if the the slide goes out or not and moves the slider
            if abs(inside_pos) > self.width:
                inside_pos = self.width

            elif inside_pos > -self.thumb.w:
                inside_pos = 0

            else:
                self.thumb.x = abs(inside_pos) - (self.thumb.w)

        # Checks click in slider thump
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pos[0] > self.x and pos[0] < self.x + self.width:
                if pos[1] > self.y and pos[1] < self.y + self.height:
                    inside_pos = self.x - pos[0]
                    if (abs(inside_pos) > self.thumb.x) and (abs(inside_pos) < self.thumb.x + self.thumb.w):
                        self.active = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.active = False


class Text_box:
    def __init__(
        self,
        x=0,
        y=1,
        width=200,
        height=100,
        bg_color=(124, 124, 124),
        active_color=(255, 255, 255),
        text_size=18,
        fg=(0, 0, 0),
        border=0,
        border_color=(0, 0, 0),
        cursor_color=(255, 0, 0),
        cursor_width=2,
    ):

        # Coords and logics
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pos = vec(self.x, self.y)
        self.size = vec(self.width, self.height)
        self.surface = pygame.Surface((width, height))
        self.active = False

        # Colors
        self.bg_color = bg_color
        self.active_color = active_color
        self.border_color = border_color
        self.fg = fg

        # Fonts
        self.text = ""
        self.textList = []
        self.text_size = text_size
        self.font = pygame.font.SysFont("Times New Roman", self.text_size)
        self.labels = []

        self.border = border

        # Cursor
        self.cursor = [0, 0]
        self.pad = 0
        self.cursor_color = cursor_color
        self.cursor_width = cursor_width

        self.inReturn = False

    def key_left(self):
        print("left")
        if sum(self.cursor) == 0:
            self.cursor = self.cursor
        elif self.cursor[0] == 0:
            self.cursor[1] -= 1
            self.cursor[0] = len(self.textList[self.cursor[1]])
        else:
            self.cursor[0] -= 1

    def multiline(self):
        text = self.text
        print(f"multiline {text.encode()}")
        self.textList = text.split("\n")
        print(self.textList, self.cursor)

    def draw(self, window):
        self.win = window
        if not self.active:
            if self.border == 0:
                self.surface.fill(self.bg_color)
            else:
                self.surface.fill(self.border_color)
                pygame.draw.rect(
                    self.surface,
                    self.bg_color,
                    (
                        self.border,
                        self.border,
                        self.width - self.border * 2,
                        self.height - self.border * 2,
                    ),
                )
                pygame.draw.rect()
        else:
            if self.border == 0:
                self.surface.fill(self.active_color)
            else:
                self.surface.fill(self.border_color)
                pygame.draw.rect(
                    self.surface,
                    self.active_color,
                    (
                        self.border,
                        self.border,
                        self.width - self.border * 2,
                        self.height - self.border * 2,
                    ),
                )
        posY = 0
        cursor = pygame.Surface((self.cursor_width, self.text_size))
        cursor.fill((self.cursor_color))

        for i in range(len(self.textList)):
            # self.pad = 0
            text = self.font.render(self.textList[i], False, self.fg)

            # getting the height and width of text
            # text_height = text.get_height()
            text_width = text.get_width()

            # drawing text into screen
            if not self.active:
                self.surface.blit(text, (self.border * 2, posY))
            else:
                if text_width < self.width - self.border * 2:
                    self.surface.blit(text, (self.border * 2, posY))
                else:
                    self.surface.blit(
                        text,
                        (
                            (self.border * 2) + (self.width - text_width - self.border * 3),
                            posY,
                        ),
                    )
            posY = (i + 1) * self.text_size
            # self.pad += text_width
            self.pad = self.font.size(self.textList[self.cursor[1]][: self.cursor[0]])[0]

        self.surface.blit(cursor, (self.pad, self.cursor[1] * self.text_size))
        window.blit(self.surface, self.pos)

    def events(self, event):
        # Checks click in box
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[0] > self.x and pos[0] < self.x + self.width:
                if pos[1] > self.y and pos[1] < self.y + self.height:
                    self.active = True

                else:
                    self.active = False

            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    if len(self.text) > 0 and self.text[-1] == "\n":
                        self.cursor[1] -= 1
                        self.cursor[0] = -1
                    self.text = self.text[: self.cursor[0] - 1] + self.text[self.cursor[0] :]
                    self.key_left()
                    print("backspace")
                elif event.key == pygame.K_RETURN:
                    self.text += "\n"
                    self.cursor[1] += 1
                    self.cursor[0] = 0
                    print("return")
                elif event.key == pygame.K_LEFT:
                    self.key_left()
                elif event.key == pygame.K_RIGHT:
                    print(self.cursor)
                    # if self.cursor[0] == 0:
                    #     self.cursor[1] -= 1
                    #     self.cursor[0] = len(self.textList[self.cursor[1]])
                    # else:
                    #     self.cursor[0] -= 1
                    print(self.cursor)
                elif str((event.unicode).encode()).find("\\") == -1:
                    if len(self.textList) > 0:
                        print(
                            "testing",
                            len(self.textList[self.cursor[1]]) + self.cursor[0],
                        )
                    self.text = self.text[: self.cursor[0]] + event.unicode + self.text[self.cursor[0] :]
                    self.cursor[0] += 1
                    print(f"letter {self.text}\nx={self.cursor[0]}\ny={self.cursor[1]}")

                self.multiline()


def gradient_rect(
    window: pygame.Surface,
    left_colour: Union[tuple, list, pygame.Color],
    right_colour: Union[tuple, list, pygame.Color],
    target_rect: pygame.Rect,
):
    """Draw a horizontal-gradient filled rectangle covering <target_rect>"""

    # Code from "https://stackoverflow.com/questions/62336555/how-to-add-color-gradient-to-rectangle-in-pygame"
    colour_rect = pygame.Surface((2, 2))
    pygame.draw.line(colour_rect, left_colour, (0, 0), (0, 1))
    pygame.draw.line(colour_rect, right_colour, (1, 0), (1, 1))
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))
    window.blit(colour_rect, target_rect)
    return colour_rect
