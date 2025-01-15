from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.lang import Builder

Builder.load_file('bird.kv')


class Bird(Image):
    velocity = NumericProperty(0)

    def move(self, dt):
        self.y += self.velocity
        if self.y < 0:
            self.y = 0

class GameScreen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bird = Bird()
        self.add_widget(self.bird)
        Clock.schedule_interval(self.update, 1/165)

    def update(self, dt):
        self.bird.move(dt)

    def on_touch_down(self, touch):
        self.bird.velocity = 10

    def on_touch_up(self, touch):
        self.bird.velocity = -5

class BirdGameApp(App):
    def build(self):
        return GameScreen()

if __name__ == '__main__':
    BirdGameApp().run()
