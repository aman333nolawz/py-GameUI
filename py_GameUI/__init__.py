"""
A Simple module for making GUIs in pygame.
You can make Buttons, Input Boxes, Sliders and gradient rectangle with this module.
"""
from typing import Union

import pygame
from pygame.event import Event

vec = pygame.math.Vector2

pygame.init()


class Settings:
    FONT = pygame.font.SysFont(None, 25)


class Button:
    """Button element"""

    def __init__(
        self,
        relative_rect: Union[pygame.Rect, tuple, list],
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
        font: pygame.font.Font = None,
        ipadx: int = 0,
        ipady: int = 0,
        function=None,
    ) -> None:
        """Initilaizes the Button element.
        params:
            relative_rect: The coordinates and the size of the button
            enabled: If you want the button to be whether enabled or disabled. Default to True
            text: The text you want to display in the button
            image: The image you want to blit
            image_x: X Coordinate of the image
            image_y: Y Coordinate of the image
            bg: The background color of the button
            fg: Color of the font
            cc: Color of the button when clicked
            hc: Color of the button when hovered
            border: The width of the border you want
            border_color: Color of the border of the Button
            border_radius: Border radius for the button
            font: Font of the text you want to display
            ipadx: The internal x-padding of the button
            ipady: The internal y-padding of the button
            function: The function you want to call when the button is pressed
        """
        # Coordinates and logics
        if isinstance(relative_rect, pygame.Rect):
            self.rect = relative_rect
        elif isinstance(relative_rect, tuple) or isinstance(relative_rect, list):
            self.rect = pygame.Rect(*relative_rect)
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
            self.border_radius = [border_radius for _ in range(4)]
        elif isinstance(border_radius, tuple):
            self.border_radius = list(border_radius)
        else:
            self.border_radius = border_radius
        self.border_color = border_color
        self.border = border

        # Font
        self.text = text
        if not font:
            self.font = Settings.FONT
        else:
            self.font = font
        self.ipadx = ipadx
        self.ipady = ipady

        # Image
        self.image = image
        self.image_x = image_x
        self.image_y = image_y

    def draw(self, win: pygame.Surface):
        """Draws the button to the screen
        params:
            win: The surface to draw the button to
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
            self._show_text()

        if self.image:
            self.surface.blit(self.image, (self.image_x, self.image_y))
        win.blit(self.surface, self.pos)

    def _show_text(self):
        """Blits the the text into screen"""
        font = self.font
        text = font.render(self.text, True, self.fg)
        size = text.get_size()
        x, y = (self.width // 2 - (size[0] // 2)) + self.ipadx, (
            self.height // 2 - (size[1] // 2)
        ) + self.ipady
        pos = vec(x, y)
        self.surface.blit(text, pos)

    def events(self, event):
        """Function to handle all the events with the button like clicking, hovering etc.
        params:
         event: Events from pygame window.
        """
        pos = pygame.mouse.get_pos()
        if (pos[0] > self.pos[0]) and (pos[0] < self.pos[0] + self.width):
            if (pos[1] > self.pos[1]) and (
                pos[1] < self.pos[1] + self.height
            ):  # Check if the mouse is hovered
                if self.enabled:
                    self.hovered = True

            else:
                self.hovered = False
        else:
            self.hovered = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if (pos[0] > self.pos[0]) and (pos[0] < self.pos[0] + self.width):
                if (pos[1] > self.pos[1]) and (
                    pos[1] < self.pos[1] + self.height
                ):  # Checks if the button is pressed
                    if self.enabled:
                        self.clicked = True

                        if self.function:
                            self.function()

        if event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False


class Input_box:
    """Input box for receiving one line input"""

    def __init__(
        self,
        relative_rect: Union[pygame.Rect, tuple, list],
        bg_color=(124, 124, 124),
        active_color=(255, 255, 255),
        font=None,
        fg=(0, 0, 0),
        border=0,
        border_color=(0, 0, 0),
    ):
        """Initilaizes the input box.
        params:
            relative_rect: Coordinates and size of the input box
            bg_color: Background color of the input box
            active_color: Background color of the input box when it is focused
            font: Font for the text
            fg: Font color for the input box
            border: Size of the border
            border_color: Color of the border
        """

        # Coords and logics
        if isinstance(relative_rect, pygame.Rect):
            self.rect = relative_rect
        elif isinstance(relative_rect, tuple) or isinstance(relative_rect, list):
            self.rect = pygame.Rect(*relative_rect)
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
        if not font:
            self.font = Settings.FONT
        else:
            self.font = font

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

        text = self.font.render(self.text, True, self.fg)

        # getting the height and width of text
        text_height = text.get_height()
        text_width = text.get_width()

        # drawing text into screen
        if not self.active:
            self.surface.blit(text, (self.border * 2, (self.height - text_height) // 2))
        else:
            if text_width < self.width - self.border * 2:
                self.surface.blit(
                    text, (self.border * 2, (self.height - text_height) // 2)
                )
            else:
                self.surface.blit(
                    text,
                    (
                        (self.border * 2)
                        + (self.width - text_width - self.border * 3),  # noqa: E501
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
        font: pygame.font.Font = None,
        show_numbers: bool = True,
    ):
        """A Slider GUI for pygame.
        params:
            x: The X position of the slider
            y: The Y position of the slider
            from_: Where The value starts from
            to_: Where the value ends
            part_size: The size for one part in the slider
            bg: Background color of the Slider
            cc: Color when the thumb is clicked
            hc: Color when the thumb is hovered
            fg: Color of the font to be displayed
            thumb_bg: Background color of the thumb
            font: The font for the number displayed
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

        if not font:
            self.font = Settings.FONT
        else:
            self.font = font

        self.value = (self.from_ - 1) + ((self.thumb.x + self.thumb.w) / self.thumb.w)
        self.show_numbers = show_numbers

    def draw(self, window: pygame.Surface):
        """A function that draws the slider into the  pygame screen
        params:
            window: The window to draw the slider to
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

        if (
            pos[0] > self.x and pos[0] < self.x + self.width
        ):  # checks if mouse's x position is inside the bar
            if (
                pos[1] > self.y and pos[1] < self.y + self.height
            ):  # checks if mouse's y position is inside the bar
                inside_pos = self.x - pos[0]
                if (abs(inside_pos) > self.thumb.x) and (
                    abs(inside_pos) < self.thumb.x + self.thumb.w
                ):  # Checks if the mouse is just over the thumb
                    self.hovering = True
                else:
                    self.hovering = False
            else:
                self.hovering = False
        else:
            self.hovering = False

        if self.active:
            inside_pos = self.x - pos[0]

            # Checks if the the slide goes out. if goes out then don't move the slider
            if abs(inside_pos) > self.width:
                inside_pos = self.width

            elif (
                inside_pos > -self.thumb.w
            ):  # Checks if thumb goes far of to the left. if yes, then set it to 0
                inside_pos = 0

            else:  # If the mouse cursor is inside the bar, then move the thumb
                self.thumb.x = abs(inside_pos) - self.thumb.w

        # Checks click in slider thump
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pos[0] > self.x and pos[0] < self.x + self.width:
                if pos[1] > self.y and pos[1] < self.y + self.height:
                    inside_pos = self.x - pos[0]
                    self.active = True
                else:
                    self.active = False
            else:
                self.active = False

        if event.type == pygame.MOUSEBUTTONUP:
            self.active = False


def gradient_rect(
    window: pygame.Surface,
    left_colour: Union[tuple, list, pygame.Color],
    right_colour: Union[tuple, list, pygame.Color],
    relative_rect: pygame.Rect,
):
    """Draw a horizontal-gradient filled rectangle covering <relative_rect>
    params:
        window: Screen to blit the gradient rect
        left_colour: Color in the left corner
        right_colour: Color in the right corner
        relative_rect: Position and width to draw the gradient rect
    """
    if isinstance(relative_rect, tuple) or isinstance(relative_rect, list):
        relative_rect = pygame.Rect(*relative_rect)
    # Code from "https://stackoverflow.com/questions/62336555/how-to-add-color-gradient-to-rectangle-in-pygame"
    colour_rect = pygame.Surface((2, 2))
    pygame.draw.line(colour_rect, left_colour, (0, 0), (0, 1))
    pygame.draw.line(colour_rect, right_colour, (1, 0), (1, 1))
    colour_rect = pygame.transform.smoothscale(
        colour_rect, (relative_rect.width, relative_rect.height)
    )
    window.blit(colour_rect, relative_rect)
    return colour_rect
