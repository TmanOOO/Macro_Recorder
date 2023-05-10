import pyautogui
import win32gui
from pywinauto.application import Application
from image_locater import locate_image as loc_image  # Renamed to avoid conflict
from pathlib import Path


def save_macro_to_batch(recorded_actions, batch_file_path, target_image_folder):
    """
    Save recorded actions to a batch file that can be executed later.
    :param recorded_actions: list of tuples containing elapsed_time and mouse_position at each mouse click
    :param batch_file_path: str representing path to location on disk where batch file will be saved
    :param target_image_folder: str representing path to location on disk where screenshot references will be saved
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

            # Send keyboard input to switch to the desired window
            win_title = 'Window Title'  # Replace this with the title of the window you want to switch to
            win32gui.SetForegroundWindow(win32gui.FindWindow(None, win_title))

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
