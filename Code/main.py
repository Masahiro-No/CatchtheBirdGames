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
from kivy.properties import ObjectProperty
import os

Builder.load_file('bird.kv')
Builder.load_file('obstacle.kv')

class mainmenu(BoxLayout): # ใช้ widget ในไฟล์ mainmenu.kv (เนื่องจากชื่อ class เดียวกัน)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ตรวจสอบ path ของไฟล์เพลง
        sound_path = os.path.join('.', 'img', 'MusicforGame', 'HSROpen.mp3')
        self.sound = SoundLoader.load(sound_path)  # โหลดไฟล์เสียง

        if self.sound:  # ตรวจสอบว่าการโหลดสำเร็จหรือไม่
            self.sound.play()
        else:
            print("Failed to load sound:", sound_path)

    def stop_music(self):  # หยุดเล่นเสียง
        if self.sound:  # ตรวจสอบว่ามีไฟล์เสียงที่โหลดอยู่หรือไม่
            self.sound.stop()

    def play_music(self):  # เล่นเพลงอีกครั้ง
        if not self.sound:  # หาก self.sound เป็น None ให้โหลดเสียงใหม่
            sound_path = os.path.join('.', 'img', 'MusicforGame', 'HSROpen.mp3')
            self.sound = SoundLoader.load(sound_path)
            if not self.sound:  # หากยังโหลดไม่ได้
                print("Failed to load sound:", sound_path)
                return

        self.sound.play()  # เล่นเพลง

class skinmenu(BoxLayout): # ใช้ widget ในไฟล์ skinmenu.kv (เนื่องจากชื่อ class เดียวกัน)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        

class Bird(Image):
    velocity = NumericProperty(0)  # ความเร็วในการเคลื่อนที่
    mask = None  # เก็บ Mask ของภาพ

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        """
        ฟังก์ชันนี้จะถูกเรียกหลังจาก Kivy โหลด widget เสร็จ
        """
        if self.source:  # ตรวจสอบว่า self.source ได้รับการกำหนดค่าแล้ว
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
    bird_mina = ObjectProperty(None)
    bird_sw = ObjectProperty(None)
    bird_danheng = ObjectProperty(None)
    bird_stelle = ObjectProperty(None)
    bird_himeko = ObjectProperty(None)
    active_bird = None

    def __init__(self, bird_id="bird_mina", **kwargs):
        super().__init__(**kwargs)
        self.select_bird(bird_id)  # เลือกนกที่ต้องการใช้งาน

        # ตรวจสอบ path ของไฟล์เพลง
        sound_path = os.path.join('.', 'img', 'MusicforGame', 'Sway to My Beat in Cosmos.mp3')
        self.sound = SoundLoader.load(sound_path)  # โหลดไฟล์เสียง

        if self.sound:  # ตรวจสอบว่าการโหลดสำเร็จหรือไม่
            self.sound.play()
        else:
            print("Failed to load sound:", sound_path)

        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        self.pressed_keys = set()


        # เก็บรายการอุปสรรคทั้งหมด
        self.obstacles = []

        # เริ่มต้นอัปเดตเกม
        Clock.schedule_interval(self.update, 1 / 60)

        # สุ่มอุปสรรคทุกๆ ช่วงเวลา
        self.spawn_obstacles()

    def stop_music(self):  # หยุดเล่นเสียง
        if self.sound:  # ตรวจสอบว่ามีไฟล์เสียงที่โหลดอยู่หรือไม่
            self.sound.stop()

    def play_music(self):  # เล่นเพลงอีกครั้ง
        if not self.sound:  # หาก self.sound เป็น None ให้โหลดเสียงใหม่
            sound_path = os.path.join('.', 'img', 'MusicforGame', 'HSROpen.mp3')
            self.sound = SoundLoader.load(sound_path)
            if not self.sound:  # หากยังโหลดไม่ได้
                print("Failed to load sound:", sound_path)
                return

        self.sound.play()  # เล่นเพลง

    def select_bird(self, bird_id):
        """เลือกนกที่ใช้งาน และลบนกที่ไม่ได้ใช้ออก"""
        # อ้างอิง bird จาก id
        self.active_bird = self.ids[bird_id]
        
        # ลบนกอื่นๆ ที่ไม่ได้เลือกออกจากหน้าจอ
        for child_id, bird_widget in self.ids.items():
            if child_id != bird_id and isinstance(bird_widget, Bird):
                self.remove_widget(bird_widget)


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
        self.active_bird.velocity = -5

    def update(self, dt):
        if self.active_bird:
            self.active_bird.move(dt)
        if 'w' in self.pressed_keys:
            self.active_bird.velocity = 10

        for obstacle in self.obstacles[:]:
            obstacle.move(dt)

            if self.active_bird.check_collision(obstacle): # ตรวจสอบการชนกัน
                print("Game Over!")
                Clock.unschedule(self.update) # หยุดอัปเดตเกม
                self.show_game_over()  # เรียกฟังก์ชันแสดง "Game Over"
                self.sound.stop() 
                return

            if obstacle.right < 0:
                self.remove_widget(obstacle)
                self.obstacles.remove(obstacle)
            
    def show_game_over(self):
        # ค้นหา Label ด้วย id
        game_over_label = self.ids.game_over_label
        game_over_label.pos = (Window.width / 2 - game_over_label.width / 2, Window.height / 2 - game_over_label.height / 2)  # กำหนดตำแหน่งของ Label
        # เปลี่ยน opacity เพื่อแสดงข้อความ
        game_over_label.opacity = 1  # แสดงข้อความ GAME OVER

        # ค้นหาปุ่ม Restart ด้วย id และแสดงมัน
        restart_button = self.ids.restart_button
        restart_button.pos = (Window.width / 2 - restart_button.width / 2, Window.height / 2 - restart_button.height / 2 - 100)  # กำหนดตำแหน่งของปุ่ม Restart
        restart_button.opacity = 1  # แสดงปุ่ม Restart

        # ค้นหาปุ่ม Close ด้วย id และแสดงมัน
        close_button = self.ids.close_button
        close_button.pos = (Window.width / 2 - close_button.width / 2, Window.height / 2 - close_button.height / 2 - 200)  # กำหนดตำแหน่งของปุ่ม Close
        close_button.opacity = 1  # แสดงปุ่ม Close

    def restart_game(self):
        # ปิดแอปพลิเคชันปัจจุบัน
        print('Restarting game...')
        App.get_running_app().stop()
        SkinMenuApp().run()  # เรียกใช้งานแอปใหม่

    def close_game(self):
        print('Thank you for playing!')
        App.get_running_app().stop()  # ปิดแอปพลิเคชันปัจจุบัน

class BirdGameApp(App):
    def __init__(self, bird_id="bird_mina", **kwargs):
        super().__init__(**kwargs)
        self.bird_id = bird_id

    def build(self):
        return GameScreen(bird_id=self.bird_id)
    

class SkinMenuApp(App):
    def build(self):
        return skinmenu()
    
    def mina_skin(self):
        self.stop()  # หยุด SkinMenuApp
        bird_game_app = BirdGameApp(bird_id="bird_mina")  # สร้าง BirdGameApp ด้วย bird_id="bird_mina"
        bird_game_app.run()  # รัน BirdGameApp

    def sw_skin(self):
        self.stop()
        bird_game_app = BirdGameApp(bird_id="bird_sw")
        bird_game_app.run()

    def danheng_skin(self):
        self.stop()
        bird_game_app = BirdGameApp(bird_id="bird_danheng")
        bird_game_app.run()

    def stelle_skin(self):
        self.stop()
        bird_game_app = BirdGameApp(bird_id="bird_stelle")
        bird_game_app.run()

    def himeko_skin(self):
        self.stop()
        bird_game_app = BirdGameApp(bird_id="bird_himeko")
        bird_game_app.run()

    def robin_skin(self):
        self.stop()
        bird_game_app = BirdGameApp(bird_id="bird_robin")
        bird_game_app.run()


class mainmenuApp(App):
    def build(self):
        return mainmenu()

    def openbirdgame(self):
        root_widget = self.root
        if root_widget and hasattr(root_widget, 'stop_music'): # ตรวจสอบว่า root_widget มีฟังก์ชัน stop_music หรือไม่
            root_widget.stop_music()
        self.stop() # หยุด App ปัจจุบัน (mainmenuApp)
        SkinMenuApp().run()
    

if __name__ == '__main__':
    mainmenuApp().run()
    