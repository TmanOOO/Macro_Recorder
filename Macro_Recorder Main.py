import time
import cv2
import os
import pyautogui
import numpy as np

def locate_image(image_path):
    # Load the target image
    target_image = cv2.imread(image_path)

    while True:
        # Take a screenshot of the screen
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Use template matching to find the target image within the screenshot
        result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Set a threshold to determine a match
        threshold = 0.8
        if max_val >= threshold:
            # Calculate the center position of the matched image
            center_x = max_loc[0] + (target_image.shape[1] // 2)
            center_y = max_loc[1] + (target_image.shape[0] // 2)

            # Perform a click action on the center position
            pyautogui.click(center_x, center_y)
            break

        # Wait for a short duration before attempting again
        time.sleep(0.5)

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

        recorded_actions.append((elapsed_time, mouse_position))

    return recorded_actions


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
            pyautogui.screenshot(target_image_path)
            locate_image(target_image_path)

        batch_file.write('echo Macro execution complete\n')
        batch_file.write('pause\n')

# Example usage
print("Recording macro...")
actions = record_macro()
print("Macro recorded successfully!")

batch_file_path = 'A:\Users\Tristan\Desktop\Main\MyCode\Macro_Recorder\Batch_Files'  # Specify the path for the batch file
target_image_folder = 'A:\Users\Tristan\Desktop\Main\MyCode\Macro_Recorder\Reference_Images'  # Specify the folder path for reference images

# Create the directory if it doesn't exist
os.makedirs(batch_file_path, exist_ok=True)
os.makedirs(target_image_folder, exist_ok=True)

save_macro_to_batch(actions, batch_file_path, target_image_folder)

print(f"Macro saved to {batch_file_path}")
