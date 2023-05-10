import time
import cv2
import os
import pyautogui
import numpy as np

from pywinauto.application import Application
from image_locater import locate_image as loc_image  # Renamed to avoid conflict
from record_macro import record_macro

def save_macro_to_batch(recorded_actions, batch_file_path, target_image_folder):
    with open(batch_file_path, 'w') as batch_file:
        batch_file.write('@echo off\n')
        batch_file.write('timeout 2\n')  # Optional delay before starting macro

        for action in recorded_actions:
            elapsed_time, mouse_position = action

            # Move the mouse to the recorded position
            batch_file.write(f'powershell.exe -Command "(New-Object -ComObject WScript.Shell).AppActivate(\'Window Title\')"\n')
            batch_file.write(f'powershell.exe -Command "$wshell = New-Object -ComObject WScript.Shell;$wshell.SendKeys(\'{{ESC}}\')"\n')
            batch_file.write(f'powershell.exe -Command "$wshell = New-Object -ComObject WScript.Shell;$wshell.SendKeys(\'{{ENTER}}\')"\n')
            batch_file.write(f'powershell.exe -Command "$wshell = New-Object -ComObject WScript.Shell;$wshell.SendKeys(\'{{TAB}}\')"\n')
            batch_file.write(f'powershell.exe -Command "$wshell = New-Object -ComObject WScript.Shell;$wshell.SendKeys(\'{{ENTER}}\')"\n')
            # Add more batch file commands for additional actions if needed

            # Locate and click on the target image
            target_image_path = os.path.join(target_image_folder, f'image_{elapsed_time}.png')
            loc_image(target_image_path)  # Use the imported function

        batch_file.write('echo Macro execution complete\n')
        batch_file.write('pause\n')

# Example usage
def main():
    print("Recording macro...")
    actions = record_macro()
    print("Macro recorded successfully!")

    batch_file_path = 'A:\Users\Tristan\Desktop\Main\MyCode\Macro_Recorder\Batch_Files'
    target_image_folder = 'A:\Users\Tristan\Desktop\Main\MyCode\Macro_Recorder\Reference_Images'

    os.makedirs(batch_file_path, exist_ok=True)
    os.makedirs(target_image_folder, exist_ok=True)

    save_macro_to_batch(actions, batch_file_path, target_image_folder)

    print(f"Macro saved to {batch_file_path}")

if __name__ == '__main__':
    main()
