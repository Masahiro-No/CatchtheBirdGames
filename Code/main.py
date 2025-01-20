from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
from PIL import Image as PILImage # Import Image class from PIL module
import random
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader

Builder.load_file('bird.kv')
Builder.load_file('obstacle.kv')

class mainmenu(BoxLayout): # ใช้ widget ในไฟล์ mainmenu.kv (เนื่องจากชื่อ class เดียวกัน)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.sound = SoundLoader.load('.\img\HSROpen.mp3') # โหลดไฟล์เสียง
        self.sound.play() # เล่นเพลง

    def stop_music(self): # หยุดเล่นเสียง
        if self.sound:
            self.sound.stop()

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

        self.sound = SoundLoader.load('.\img\Sway to My Beat in Cosmos.mp3')
        self.sound.play()

        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        self.pressed_keys = set()

        # ตัวละคร Bird
        self.bird = Bird()
        self.add_widget(self.bird)

        # เก็บรายการอุปสรรคทั้งหมด
        self.obstacles = []

        # เริ่มต้นอัปเดตเกม
        Clock.schedule_interval(self.update, 1 / 60)

        # สุ่มอุปสรรคทุกๆ ช่วงเวลา
        self.spawn_obstacles()

    def spawn_obstacles(self, *args):
        # สุ่มจำนวนอุปสรรคใหม่ในรอบนี้ (เช่น 1 ถึง 2 อัน)
        num_obstacles = random.randint(1, 2)

        for _ in range(num_obstacles):
            obstacle = Obstacle_1()

            max_y = Window.height - obstacle.height  # ขอบบนสุดที่อุปสรรคอยู่ได้
            y_position = random.randint(0, max_y)  # สุ่ม y ในช่วงที่ไม่หลุดจอ

            obstacle = Obstacle_1(pos=(Window.width, y_position))
            self.add_widget(obstacle)
            self.obstacles.append(obstacle)

        # สุ่มเวลาสำหรับการเกิดอุปสรรคใหม่
        next_spawn_time = random.uniform(1, 5)  # สุ่มเวลา 1 ถึง 2 วินาที
        Clock.schedule_once(self.spawn_obstacles, next_spawn_time)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.pressed_keys.add(keycode[1])

    def _on_key_up(self, keyboard, keycode):
        if keycode[1] in self.pressed_keys:
            self.pressed_keys.remove(keycode[1])
        self.bird.velocity = -5

    def update(self, dt):
        self.bird.move(dt)
        if 'w' in self.pressed_keys:
            self.bird.velocity = 10

        for obstacle in self.obstacles[:]:
            obstacle.move(dt)

            if self.bird.check_collision(obstacle): # ตรวจสอบการชนกัน
                print("Game Over!")
                Clock.unschedule(self.update) # หยุดอัปเดตเกม
                self.sound.stop() 
                return

            if obstacle.right < 0:
                self.remove_widget(obstacle)
                self.obstacles.remove(obstacle)

class BirdGameApp(App):
    def build(self):
        return GameScreen()


class mainmenuApp(App):
    def build(self):
        return mainmenu()
    
    def openbirdgame(self):
        root_widget = self.root
        if root_widget and hasattr(root_widget, 'stop_music'): # ตรวจสอบว่า root_widget มีฟังก์ชัน stop_music หรือไม่
            root_widget.stop_music()
        self.stop() # หยุด App ปัจจุบัน (mainmenuApp)
        BirdGameApp().run()
    

if __name__ == '__main__':
    mainmenuApp().run()
    