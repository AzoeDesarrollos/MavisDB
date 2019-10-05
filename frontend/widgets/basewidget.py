from pygame.sprite import DirtySprite


class BaseWidget(DirtySprite):
    active = False

    def __init__(self, image, rect):
        super().__init__()
        self.image = image
        self.rect = rect

    def on_keydown(self, key):
        pass

    def on_keyup(self, key):
        pass

    def on_mousebuttondown(self, button):
        pass

    def on_mousebuttonup(self, button):
        pass

    def on_mousemotion(self):
        pass

    def on_mouseover(self):
        pass

    def update(self):
        pass
