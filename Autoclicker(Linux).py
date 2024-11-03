# Make sure you install the following libraries on your linux system
# pip install opencv-python-headless mss numpy pygetwindow pyautogui keyboard

import os
import time
import random
import cv2
import keyboard
import mss
import numpy as np
import pygetwindow as gw
import pyautogui
import warnings

CHECK_INTERVAL = 5

warnings.filterwarnings("ignore", category=UserWarning)

# Target color (in hex) for normal gameplay elements
target_colors_hex = ["#abff61", "#87ff27"]
nearby_colors_hex = ["#9eff00", "#b0ff50"]
threshold = 0.8

# Define color conversion functions
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def color_distance(color1, color2):
    return np.linalg.norm(np.array(color1) - np.array(color2))

target_colors_rgb = [hex_to_rgb(color) for color in target_colors_hex]
nearby_colors_rgb = [hex_to_rgb(color) for color in nearby_colors_hex]

# Linux-compatible function for mouse clicks using pyautogui
def click_at(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()

# Screen capture and object detection function
def find_target_position(screen):
    img_rgb = np.array(screen)
    img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV)

    for y in range(img_hsv.shape[0]):
        for x in range(img_hsv.shape[1]):
            pixel_rgb = img_rgb[y, x][:3]
            for target_rgb in target_colors_rgb:
                distance = color_distance(pixel_rgb, target_rgb)
                if distance < threshold * 255:  # Adjusted threshold check
                    return x, y
    return None, None

# Main game loop
def main():
    while True:
        try:
            if keyboard.is_pressed("q"):
                print("Quitting...")
                break
            
            windows = gw.getWindowsWithTitle("Telegram")
            if not windows:
                print("Telegram window not found.")
                time.sleep(CHECK_INTERVAL)
                continue
            
            telegram_window = windows[0]
            telegram_window.activate()
            bbox = (telegram_window.left, telegram_window.top, telegram_window.right, telegram_window.bottom)

            with mss.mss() as sct:
                screen = sct.grab(bbox)
                x, y = find_target_position(screen)
                if x is not None and y is not None:
                    click_at(x + telegram_window.left, y + telegram_window.top)
                    time.sleep(random.uniform(0.1, 0.3))
                else:
                    print("Target not found.")
                    
            time.sleep(CHECK_INTERVAL)
        
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    print("Starting Blum minigame bot for Linux. Press 'q' to quit.")
    main()
