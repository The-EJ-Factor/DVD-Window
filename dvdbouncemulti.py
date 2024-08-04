import pygetwindow
import keyboard
import win32api
import time
import win32gui
import math
import random

toggleKey = 'shift+\\'
exitkey = 'End'


class WindowBounceEffect:
    def __init__(self, window):
        self.window = window
        self.bouncing = False
        self.speed = (random.random() * 2 + 1) * ((random.random()>0.5)*2 - 1)
        self.randnum = random.random() * math.pi
        self.direction_x, self.direction_y = math.cos(self.randnum), math.sin(self.randnum)
        self.x, self.y, self.width, self.height = self.window.left, self.window.top, self.window.width, self.window.height

    def toggle_bounce(self):
        self.bouncing = not self.bouncing
        if self.bouncing:
            self.speed = (random.random() * 4 + 1) * ((random.random()>0.5)*2 - 1)
            self.randnum = random.random() * math.pi
            self.direction_x, self.direction_y = math.cos(self.randnum), math.sin(self.randnum)
            self.x, self.y, self.width, self.height = self.window.left, self.window.top, self.window.width, self.window.height


    def update_position(self):
        if self.bouncing:
            if self.x <= 0 or self.x + self.width >= win32api.GetSystemMetrics(0):
                self.direction_x *= -1
            if self.y <= 0 or self.y + self.height >= win32api.GetSystemMetrics(1):
                self.direction_y *= -1   

            self.x += self.speed * self.direction_x
            self.y += self.speed * self.direction_y

            self.window.moveTo(int(self.x), int(self.y))



def main():
    cantoggle = True
    windows = pygetwindow.getAllWindows()
    window_effects = [(window, WindowBounceEffect(window)) for window in windows]
    selected_window = None

    while True:
        if keyboard.is_pressed(exitkey):
            break

        if keyboard.is_pressed(toggleKey) and cantoggle:
            active_window = pygetwindow.getActiveWindow()
            cantoggle = False
            for window, effect in window_effects:
                if window == active_window:
                    selected_window = window
                    effect.toggle_bounce()
        
        if not keyboard.is_pressed(toggleKey) and not cantoggle:
            cantoggle = True

        if selected_window:
            for window, effect in window_effects:
                effect.update_position()\

        time.sleep(0.02)

if __name__ == "__main__":
    main()