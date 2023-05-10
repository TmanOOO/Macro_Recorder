import time
import cv2
import os
import pyautogui
import win32gui
import numpy as np
from pathlib import Path
from pywinauto.application import Application
from image_locater import locate_image as loc_image  # Renamed to avoid conflict
from record_macro import record_macro
from batch_saver import save_macro_to_batch


def main():
    """
    Main function that calls the other functions to record a macro and save it to a batch file.
    """

    print("Recording macro...")
    actions = record_macro()
    print("Macro recorded successfully!")

    # Define paths for saving batch file and image references
    batch_file_path = Path.cwd() / 'Macro_Recorder' / 'Batch_Files'
    target_image_folder = Path.cwd() / 'Macro_Recorder' / 'Reference_Images'

    # Make directories if they don't exist already
    batch_file_path.mkdir(parents=True, exist_ok=True)
    target_image_folder.mkdir(parents=True, exist_ok=True)

    save_macro_to_batch(actions, str(batch_file_path / 'macro.bat'), str(target_image_folder))

    print(f"Macro saved to {batch_file_path}")


if __name__ == '__main__':
    main()