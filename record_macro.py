import time
import cv2
import os
import pyautogui
import numpy as np

def record_macro():
    recorded_actions = []
    start_time = time.time()

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        # Capture mouse position
        mouse_position = pyautogui.position()

        # Capture keyboard events
        if pyautogui.keyIsDown('esc'):
            break  # Stop recording if the 'esc' key is pressed
            
        # Capture screenshot and save it
        target_image_folder = os.path.join(os.path.dirname(__file__), 'reference_images')
        target_image_path = os.path.join(target_image_folder, f'image_{elapsed_time}.png')
        screenshot = pyautogui.screenshot()
        cv2.imwrite(target_image_path, np.array(screenshot))

        recorded_actions.append((elapsed_time, mouse_position))

    return recorded_actions
