import os
from pathlib import Path
import time

import cv2
import numpy as np
import pyautogui
from pywinauto.application import Application

# Add the new code below this line
import sys

if sys.platform == 'win32':
    # Windows-specific code
    import win32gui
elif sys.platform == 'darwin':
    # macOS-specific code
    import Cocoa
else:
    raise NotImplementedError(f"Unsupported platform: {sys.platform}")

import subprocess
# Install required packages using pip
subprocess.check_call(["pip", "install", "-r", "requirements.txt"])

from batch_saver import save_macro_to_batch
from image_locater import locate_image as loc_image  # renamed to avoid conflict
from record_macro import record_macro


def main():
    """
    Main function that calls the other functions to record a macro and save it to a batch file.
    """
    try:
        print("Recording macro...")
        actions = record_macro()
        if not actions:
            raise ValueError("No actions recorded")

        print("Macro recorded successfully!")

        # Define paths for saving batch file and image references
        current_directory = Path.cwd()
        batch_file_path = current_directory / 'Macro_Recorder' / 'Batch_Files'
        target_image_folder = current_directory / 'Macro_Recorder' / 'Reference_Images'

        # Create directories if they don't exist already
        batch_file_path.mkdir(parents=True, exist_ok=True)
        target_image_folder.mkdir(parents=True, exist_ok=True)

        save_macro_to_batch(actions, str(batch_file_path / 'macro.bat'), str(target_image_folder))

        print(f"Macro saved to {batch_file_path}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
