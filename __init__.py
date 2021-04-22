import pygame

vec = pygame.math.Vector2

pygame.init()


class Button:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        enabled: bool = True,
        text: str = "",
        bg: tuple = (124, 124, 124),
        fg: tuple = (255, 255, 255),
        cc: tuple = (13, 80, 213),
        hc: tuple = (160, 160, 160),
        border: int = 2,
        border_color: tuple = (0, 0, 0),
        font: pygame.font = pygame.font.SysFont("arial", 25),
        ipadx: int = 0,
        ipady: int = 0,
        function=None,
    ):

        # Coordinates and logics
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pos = vec(x, y)
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.enabled = enabled
        self.function = function
        self.hovered = False
        self.clicked = False

        # Colors
        self.bg = bg
        self.fg = fg
        self.hc = hc
        self.cc = cc
        self.border_color = border_color
        self.border = border

        # Font
        self.text = text
        self.font = font
        self.ipadx = ipadx
        self.ipady = ipady

    def draw(self, win):
        if self.border != 0:
            self.image.fill(self.border_color)

            if self.clicked:
                pygame.draw.rect(
                    self.image,
                    self.cc,
                    (
                        self.border,
                        self.border,
                        self.width - (self.border * 2),
                        self.height - (self.border * 2),
                    ),
                )
            elif self.hovered:
                pygame.draw.rect(
                    self.image,
                    self.hc,
                    (
                        self.border,
                        self.border,
                        self.width - (self.border * 2),
                        self.height - (self.border * 2),
                    ),
                )
            else:
                pygame.draw.rect(
                    self.image,
                    self.bg,
                    (
                        self.border,
                        self.border,
                        self.width - (self.border * 2),
                        self.height - (self.border * 2),
                    ),
                )

        else:
            self.image.fill(self.bg)

        if len(self.text) > 0:
            self.show_text()

        win.blit(self.image, self.pos)

    def show_text(self):
        font = self.font
        text = font.render(self.text, False, self.fg)
        size = text.get_size()
        x, y = (self.width // 2 - (size[0] // 2)) + self.ipadx, (
            self.height // 2 - (size[1] // 2)
        ) + self.ipady
        pos = vec(x, y)
        self.image.blit(text, pos)

    def events(self, event):
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

            if (position[0] > self.pos[0]) and (position[0] < self.pos[0] + self.width):
                if (position[1] > self.pos[1]) and (
                    position[1] < self.pos[1] + self.height
                ):
                    if self.enabled:
                        self.clicked = True

                        if self.function:
                            self.function()

        if event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False


class Input_box:
    def __init__(
        self,
        x=0,
        y=0,
        width=75,
        height=30,
        bg_color=(124, 124, 124),
        active_color=(255, 255, 255),
        font_size=18,
        fg=(0, 0, 0),
        border=0,
        border_color=(0, 0, 0),
    ):

        # Coords and logics
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pos = vec(x, y)
        self.size = vec(width, height)
        self.image = pygame.Surface((width, height))
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
        if not self.active:
            if self.border == 0:
                self.image.fill(self.bg_color)
            else:
                self.image.fill(self.border_color)
                pygame.draw.rect(
                    self.image,
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
                self.image.fill(self.active_color)
            else:
                self.image.fill(self.border_color)
                pygame.draw.rect(
                    self.image,
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
            self.image.blit(text, (self.border * 2, (self.height - text_height) // 2))
        else:
            if text_width < self.width - self.border * 2:
                self.image.blit(
                    text, (self.border * 2, (self.height - text_height) // 2)
                )
            else:
                self.image.blit(
                    text,
                    (
                        (self.border * 2) + (self.width - text_width - self.border * 3),
                        (self.height - text_height) // 2,
                    ),
                )

        window.blit(self.image, self.pos)

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
        font: pygame.font = pygame.font.SysFont("arial", 16),
        show_numbers: bool = True,
    ):
        """A Slider GUI for pygame.
        params:
            x: int                                               #The x coordinate of slider
            y: int                                               #The y coordinate of slider
            # Where The value starts from
            from_: int  default=0
            to_: int = 3                                         #Where The value ends
            # The size for one part in the slider
            part_size: int  default = 10
            # Background color of the Slider
            bg: tuple   default = (54, 54, 54)
            # Color when the thumb is clicked
            cc: tuple   default = (13, 80, 213)
            # Color when the thumb is hovered
            hc: tuple   default = (160, 160, 160)
            # Color of the font to be displayed
            fg: tuple   default = (255, 255, 255)
            # Background color of the thumb
            thumb_bg: tuple     default = (124, 124, 124)
            # the font of the numbers
            font: pygame.font   default = pygame.font.SysFont("arial", 16)
            # True if you want the numbers to be shown
            show_numbers: bool  default = True
        """

        self.x = x
        self.y = y
        self.pos = vec(x, y)
        self.from_ = from_
        self.to_ = to_
        self.width = to_ * part_size
        self.height = 25
        self.image = pygame.Surface((self.width, self.height))
        self.active = False
        self.hovering = False

        thumb_width = self.width // (to_ - (from_ - 1))
        self.thumb = pygame.Rect(0, 0, thumb_width, self.height)

        self.bg = bg
        self.hc = hc
        self.cc = cc
        self.thumb_bg = thumb_bg
        self.fg = fg

        self.font = font

        self.value = (self.from_ - 1) + ((self.thumb.x + self.thumb.w) / self.thumb.w)
        self.show_numbers = show_numbers

    def draw(self, window):
        """A function that draws the slider into the  pygame screen"""

        self.value = (self.from_ - 1) + ((self.thumb.x + self.thumb.w) / self.thumb.w)
        self.image.fill(self.bg)

        if self.active:
            pygame.draw.rect(self.image, self.cc, self.thumb)
        elif self.hovering:
            pygame.draw.rect(self.image, self.hc, self.thumb)
        else:
            pygame.draw.rect(self.image, self.thumb_bg, self.thumb)

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

        window.blit(self.image, self.pos)

    def events(self, event):
        """A function to handle all events like clicking, moving, hovering and more"""

        pos = pygame.mouse.get_pos()

        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                inside_pos = self.x - pos[0]
                if (abs(inside_pos) > self.thumb.x) and (
                    abs(inside_pos) < self.thumb.x + self.thumb.w
                ):
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
                    if (abs(inside_pos) > self.thumb.x) and (
                        abs(inside_pos) < self.thumb.x + self.thumb.w
                    ):
                        self.active = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.active = False
