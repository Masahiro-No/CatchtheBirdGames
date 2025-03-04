# Catch The Bird Game
เป็นเกมแนวหลบอุปสรรคซึ่งผู้เล่นจะต้องควบคุมตัวละครนกเพื่อหลบอุปสรรคให้ได้นานที่สุดโดยที่จะแพ้เมื่อหลบอุปสรรคไม่สำเร็จ สร้างขึ้นโดยใช้ภาษา Python และใช้ Library kivy นอกจากนี้เกมยังมีสกินนกหลายแบบ เมนูหลัก และเมนูเลือกสกิน รวมถึงเสียงเพลงพื้นหลังและเอฟเฟกต์เสียงอีกด้วย


# Game Overall

ผู้เล่นจะได้รับบทเป็นตัวละคร Bird ซึ่งจะต้องหลบอุปสรรคที่วิ่งเข้ามาจากมางด้านขวาของหน้าจอ โดยที่หากหลบไม่สำเร็จจะถือว่า Game Over ทันที โดยที่อุปสรรคที่วิ่งเข้ามานั้นจะเพิ่มความเร็วขึ้นในทุกๆ 1 วินาที และเมื่อผู้เล่นเห็นว่าไม่สามารถหลบได้ ก็สามารถหลีกเลี่ยงอุปสรรคเหล่านั้นได้ด้วยการกด Click ที่ตัวอุปสรรคและอุปสรรคนั้นก็จะหายไป

## Features of Game
-   **เมนูหลัก**: เกมเริ่มต้นด้วยเมนูหลักที่ผู้เล่นสามารถเริ่มเกมหรือออกจากเกม
-   **การเลือกสกิน**: ผู้เล่นสามารถเลือกสกินนกได้หลายแบบก่อนเริ่มเกม
-   **การหลบหลีกสิ่งกีดขวาง**: ผู้เล่นควบคุมนกให้หลบหลีกสิ่งกีดขวางที่เข้ามา
-   **การตรวจจับการชน**: เกมใช้การตรวจจับการชนที่แม่นยำถึงระดับพิกเซล
-   **ความยากที่เพิ่มขึ้น**: ความเร็วของสิ่งกีดขวางจะเพิ่มขึ้นตามเวลา ทำให้เกมยากขึ้น
-   **หน้าจอเกมโอเวอร์**: เมื่อชนกับสิ่งกีดขวาง จะมีหน้าจอเกมโอเวอร์พร้อมตัวเลือกให้เริ่มใหม่หรือปิดเกม

## File Structure

-   **main.py**: สคริปต์หลักสำหรับรันเกม
-   **bird.kv**: ไฟล์ Kivy สำหรับกำหนด UI และพฤติกรรมของนก, กำหนด UI และพฤติกรรมของ SkinmenuApp และกำหนด UI และพฤติกรรมของ GameScreen
-   **mainmenu.kv**: ไฟล์ Kivy สำหรับกำหนด UI และพฤติกรรมของหน้า MainmenuApp
-   **obstacle.kv**: ไฟล์ Kivy สำหรับกำหนด UI และพฤติกรรมของสิ่งกีดขวาง
-   **img**: โฟลเดอร์ที่เก็บภาพและเพลงที่ใช้ในเกม

## How to Plays?

เริ่มต้นจากการที่เมื่อเริ่มเกม ผู้เล่นจะเข้าสู่หน้า Mainmenu App ก่อน ซึ่งหน้านี้จะมีปุ่มอยู่สามชิ้นคือ Start Game, Stop Music, Play Music เมื่อผู้เล่นกด Start Game ก็จะเข้าสู่หน้าถัดไป คือ Skinmenu App โดยที่จะให้ผู้เล่นเลือกตัวละคร Bird ที่อยากเล่นเพื่อที่จะใช้ในการเล่นตัวเกมผ่านการกดปุ่มใต้รูปเหล่านั้น เมื่อกดปุ่มแล้วก็จะเข้าสู่หน้าถัดไป คือ GameScreen ซึ่งจะเป็นหน้าของตัวเกม โดยที่
1. ผู้เล่นจะเป็นตัวละคร Bird ตามที่เลือกมา และต้องหลบอุปสรรคโดยการกดปุ่ม W เพื่อบินขึ้นเพื่อหลบอุปสรรค
2. อุปสรรคจะเข้ามาจากทางขวามือของหน้าจอ โดยที่เมื่อเวลาผ่านไปอุปสรรคจะเร็วขึ้นเรื่อยๆทุก 1 วินาที
3.  ผู้เล่นสามารถทำการลบอุปสรรคได้ด้วยการกด Click ที่ตัวอุปสรรคที่ต้องการลบ และอุปสรรคนั้นจะหายไป
### Summary of How to plays
1.  **เริ่มเกม**: รันสคริปต์ `main.py` เพื่อเริ่มเกม
2.  **เมนูหลัก**: ใช้เมนูหลักเพื่อเริ่มเกมหรือออกจากเกม
3.  **เลือกสกิน**: เลือกสกินนกจากเมนูเลือกสกิน
4.  **การเล่นเกม**: กดปุ่ม W เพื่อบังคับให้นกบินขึ้น หลีกเลี่ยงสิ่งกีดขวางให้นานที่สุด
5.  **เกมโอเวอร์**: เมื่อชนสิ่งกีดขวาง หน้าจอเกมโอเวอร์จะปรากฏขึ้น คุณสามารถเลือกเริ่มเกมใหม่หรือปิดเกม
