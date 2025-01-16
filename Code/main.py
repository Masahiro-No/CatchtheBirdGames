from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
from PIL import Image as PILImage # Import Image class from PIL module

Builder.load_file('bird.kv')
Builder.load_file('obstacle.kv')

class Bird(Image):
    velocity = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mask = self.create_mask(self.source)  # สร้าง Mask จากภาพ Bird

    def move(self, dt):
        self.y += self.velocity
        if self.y < 0:
            self.y = 0
        elif self.top > Window.height:
            self.top = Window.height

    def create_mask(self, image_path):
        pil_image = PILImage.open(image_path).convert('L')  # เปลี่ยนเป็น grayscale
        mask = pil_image.point(lambda p: p > 0 and 255)  # สร้าง Mask (255 = ชนได้, 0 = โปร่งใส)
        return mask

    def check_collision(self, obstacle):
        # ตรวจสอบว่ากล่องสี่เหลี่ยมชนกันก่อน
        if not self.collide_widget(obstacle):
            return False
        
        # คำนวณตำแหน่งที่ซ้อนทับกัน
        x_overlap = max(0, min(self.right, obstacle.right) - max(self.x, obstacle.x))
        y_overlap = max(0, min(self.top, obstacle.top) - max(self.y, obstacle.y))
        if x_overlap == 0 or y_overlap == 0:
            return False

        # คำนวณพิกเซลใน Mask
        for x in range(int(x_overlap)):
            for y in range(int(y_overlap)):
                bird_mask_x = int((x + max(self.x, obstacle.x) - self.x) / self.width * self.mask.size[0])
                bird_mask_y = int((y + max(self.y, obstacle.y) - self.y) / self.height * self.mask.size[1])
                obstacle_mask_x = int((x + max(self.x, obstacle.x) - obstacle.x) / obstacle.width * obstacle.mask.size[0])
                obstacle_mask_y = int((y + max(self.y, obstacle.y) - obstacle.y) / obstacle.height * obstacle.mask.size[1])

                if (
                    0 <= bird_mask_x < self.mask.size[0]
                    and 0 <= bird_mask_y < self.mask.size[1]
                    and 0 <= obstacle_mask_x < obstacle.mask.size[0]
                    and 0 <= obstacle_mask_y < obstacle.mask.size[1]
                ):
                    if (
                        self.mask.getpixel((bird_mask_x, bird_mask_y)) > 0
                        and obstacle.mask.getpixel((obstacle_mask_x, obstacle_mask_y)) > 0
                    ):
                        return True
        return False


class Obstacle_1(Image):
    def move(self, dt):
        self.x -= 200 * dt
        if self.right < 0:
            self.x = Window.width

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mask = self.create_mask(self.source)

    def create_mask(self, image_path):
        pil_image = PILImage.open(image_path).convert('L')
        mask = pil_image.point(lambda p: p > 0 and 255)
        return mask


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

        self.obstacle_1 = Obstacle_1(pos=(Window.width, 200))
        self.add_widget(self.obstacle_1)

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
        self.obstacle_1.move(dt)
        step = 1000 * dt
        if 'w' in self.pressed_keys:
            self.bird.velocity = 10

        if self.bird.check_collision(self.obstacle_1):
            print("Game Over!")
            self.bird.velocity = 0
            Clock.unschedule(self.update)


class BirdGameApp(App):
    def build(self):
        return GameScreen()

if __name__ == '__main__':
    BirdGameApp().run()
    