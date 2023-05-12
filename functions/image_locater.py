import cv2
import time
import numpy as np
import pyautogui
import win32gui  

def locate_image(image_path):
    try:
        # Load the target image
        target_image = cv2.imread(image_path)
        
        # Check if the image was loaded successfully
        if target_image is None:
            raise ValueError("Could not load image at: {}".format(image_path))
        
        # Enumerate all windows
        def window_callback(hwnd, screenshot):
            rect = win32gui.GetWindowRect(hwnd)
            x, y, width, height = rect
            if x >= 0 and y >= 0 and width > 0 and height > 0:
                # Take a screenshot of the window and convert it to BGR format
                img = np.array(pyautogui.screenshot(region=rect))
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                screenshot.append(img)
        
        screenshots = []
        win32gui.EnumWindows(window_callback, screenshots)

        # Iterate over all screenshots and look for a match
        for screenshot in screenshots:
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
        
    except Exception as e:
        print("Error occurred:", str(e))
