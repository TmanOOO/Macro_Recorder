import time
import cv2
import os
import pyautogui
import numpy as np
from pathlib import Path
from pywinauto.application import Application
from image_locater import locate_image as loc_image  # Renamed to avoid conflict
from record_macro import record_macro

def save_macro_to_batch(recorded_actions, batch_file_path, target_image_folder):
    """
    Save recorded actions to a batch file that can be executed later.
    """
    with open(batch_file_path, 'w') as batch_file:
        batch_file.write('@echo off\n')
        batch_file.write('timeout 2\n')  # Optional delay before starting macro

        app = Application().start('path/to/application.exe')
        main_window = app.Dialog

        for action in recorded_actions:
            elapsed_time, mouse_position = action

            # Move the mouse to the recorded position
            pyautogui.moveTo(mouse_position[0], mouse_position[1])

            # Send keyboard input to the target window
            main_window.type_keys('{ESC}')
            main_window.type_keys('{ENTER}')
            main_window.type_keys('{TAB}')
            main_window.type_keys('{ENTER}')
            # Add more batch file commands for additional actions if needed

            # Locate and click on the target image
            target_image_path = Path(target_image_folder) / f'image_{elapsed_time}.png'
            loc_image(str(target_image_path))  # Use the imported function

            # Perform action on target window using pywinauto
            child_control = main_window.child_window(title='Child Control Title')
            child_control.click_input()

        batch_file.write('echo Macro execution complete\n')
        batch_file.write('pause\n')

def main():
    print("Recording macro...")
    actions = record_macro()
    print("Macro recorded successfully!")

    batch_file_path = Path.cwd() / 'Macro_Recorder' / 'Batch_Files'
    target_image_folder = Path.cwd() / 'Macro_Recorder' / 'Reference_Images'

    batch_file_path.mkdir(parents=True, exist_ok=True)
    target_image_folder.mkdir(parents=True, exist_ok=True)

    save_macro_to_batch(actions, str(batch_file_path / 'macro.bat'), str(target_image_folder))

    print(f"Macro saved to {batch_file_path}")

if __name__ == '__main__':
    main()
