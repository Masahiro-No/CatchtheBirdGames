from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window

Builder.load_file('bird.kv')


class Bird(Image):
    velocity = NumericProperty(0)
    
    def move(self, dt):
        self.y += self.velocity
        if self.y < 0:
            self.y = 0
        elif self.top > Window.height:
            self.top = Window.height

class GameScreen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._keyboard = Window.request_keyboard(
                self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        self.pressed_keys = set()

        self.bird = Bird()
        self.add_widget(self.bird)
        Clock.schedule_interval(self.update, 1/165)
    
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, verified):
        self.pressed_keys.add(keycode[1])
            
    def _on_key_up(self, keyboard, keycode):
        if keycode[1] in self.pressed_keys:
            self.pressed_keys.remove(keycode[1])
        self.bird.velocity = -5


    def update(self, dt):
        self.bird.move(dt)
        step = 1000 * dt
        if 'w' in self.pressed_keys:
            self.bird.velocity = 10

class BirdGameApp(App):
    def build(self):
        return GameScreen()

if __name__ == '__main__':
    BirdGameApp().run()
