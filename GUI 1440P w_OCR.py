# V2.4 Changes:
# Fixed sleep function & added 3 screenshots each loop
# Works as intended
# Still has false positives


import tkinter as tk
import pyautogui
import time
import random
import numpy as np
import string
from pynput import keyboard
import pytesseract
from PIL import Image

# Function to perform OCR on the specific area of the screen
def ocr_screen_text():
    # Capture the specific area of the screen where the "World Locked by" information is displayed
    left, top, width, height = (116, 4, 2197, 310)
    screenshot = pyautogui.screenshot(region=(left, top, width, height))

    # Convert the screenshot to grayscale for better OCR performance
    screenshot_gray = screenshot.convert('L')

    # Use pytesseract to extract text from the image
    extracted_text = pytesseract.image_to_string(screenshot_gray)

    # Write the extracted text to a file
    with open("extracted_text.txt", "a") as file:
        file.write(extracted_text)

    return extracted_text

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.is_running = False
        self.listener = None
        self.status_label = None

    def create_widgets(self):
        self.length_label = tk.Label(self, text="Length:")
        self.length_label.pack(side="left")

        self.length_entry = tk.Entry(self)
        self.length_entry.pack(side="left")

        self.iterations_label = tk.Label(self, text="Iterations:")
        self.iterations_label.pack(side="left")

        self.iterations_entry = tk.Entry(self)
        self.iterations_entry.pack(side="left")

        self.generate_button = tk.Button(self, text="Generate", command=self.generate)
        self.generate_button.pack(side="left")

        self.status_label = tk.Label(self, text="")
        self.status_label.pack(side="bottom")

    def generate(self):
        length = self.length_entry.get()
        iterations = self.iterations_entry.get()

        try:
            length = int(length)
            iterations = int(iterations)
        except ValueError:
            self.error_message("Please enter a number")
            return

        try:
            if length < 1 or length > 10:
                raise ValueError("Please enter a number between 1 and 10")

            if iterations < 1:
                raise ValueError("Please enter a positive number of iterations")

            rand_list = self.generate_random(iterations, length)
            self.run_macro(rand_list)
        except ValueError as e:
            self.error_message(str(e))

    def generate_random(self, iterations, length):
        rand_list = []
        if iterations > 100:
            print(
                "Warning: your selected number of iterations is greater than 100. This may lead to complications in search procedure.")
            for x in range(iterations):
                rand = ''
                for i in range(length):
                    rand += random.choice(string.ascii_letters + string.digits)
                rand_list.append(rand)
            return rand_list
        else:
            for x in range(iterations):
                rand = ''
                for i in range(length):
                    rand += random.choice(string.ascii_letters + string.digits)
                rand_list.append(rand)
            return rand_list

    def run_macro(self, rand_list):
        global on_release
        def on_release(key):
            if key == keyboard.Key.pause:
                self.stop_macro()
                return False

        self.is_running = True
        last_world_name = None  # To store the last world name used

        with keyboard.Listener(on_release=on_release) as self.listener:
            while self.is_running:
                # Get the next world name from rand_list
                global next_world_name
                next_world_name = rand_list.pop(0)
                global last_world_name
                last_world_name = next_world_name

                # Perform the usual macro actions with the new world name
                pyautogui.click(2259, 117)
                time.sleep(1)
                pyautogui.click(1695, 388)
                pyautogui.press('backspace')
                pyautogui.press('backspace')
                pyautogui.press('backspace')
                for y in range(len(next_world_name)):
                    pyautogui.press('backspace')
                time.sleep(0.1)
                pyautogui.typewrite(next_world_name)
                pyautogui.press('enter')

                # Wait for the world to load before capturing the screenshot
                time.sleep(3)  # Adjust the duration based on the average world loading time in your location (depends on latency & wifi speed)

                # Capture the whole screen
                screenshot = pyautogui.screenshot()

                # Convert the screenshot to a NumPy array
                unseen_image = np.array(screenshot)

                # Use pytesseract to extract text from the specific area of the screen
                extracted_text1 = ocr_screen_text()

                time.sleep(1)

                # Capture the whole screen
                screenshot = pyautogui.screenshot()

                # Convert the screenshot to a NumPy array
                unseen_image = np.array(screenshot)

                # Use pytesseract to extract text from the specific area of the screen
                extracted_text2 = ocr_screen_text()

                time.sleep(1)

                # Capture the whole screen
                screenshot = pyautogui.screenshot()

                # Convert the screenshot to a NumPy array
                unseen_image = np.array(screenshot)

                # Use pytesseract to extract text from the specific area of the screen
                extracted_text3 = ocr_screen_text()

                # Reason we take 3 screenshots is to improve OCR accuracy
                # 1 Screenshot leaves room for the OCR to not read a letter properly, or make a mistake
                # 3 Screenshots significantly reduce that chance
                extracted_text = extracted_text3 + extracted_text2 + extracted_text1

                # If the extracted text contains "Locked" report the world as taken (Class 1)
                if "locked" in extracted_text or "Locked" in extracted_text:
                    predicted_class = 1
                else:
                    predicted_class = 0

                pyautogui.click(2443, 117)
                time.sleep(0.2)
                pyautogui.click(1328, 252)  # Replace with your X and Y coordinates
                time.sleep(0.1)

                # If the world is not taken (Class 0) or locked, save the last world name to the text file
                if predicted_class == 0 and last_world_name is not None:
                    with open("unseen_worlds.txt", "a") as file:
                        file.write(last_world_name + "\n")


    def stop_macro(self):
        if self.is_running:
            self.is_running = False
            self.listener.stop()
            print("Macro stopped.")

    # Function to go over worlds inside txt file to double check they are not false positives
    # Works but still has some bugs. Wouldn't recommend using this function if you are going to have a lot of iterations
    def double_check(self):
        updated_worlds = []
        with open("unseen_worlds.txt", "a") as file:
            unseen_worlds = file.readlines()
        for world_name in unseen_worlds:
            world_name = world_name.strip()
            with keyboard.Listener(on_release=on_release) as self.listener:
                while self.is_running:

                    # Perform the usual macro actions with the new world name
                    pyautogui.click(2259, 117)
                    time.sleep(1)
                    pyautogui.click(1695, 388)
                    pyautogui.press('backspace')
                    pyautogui.press('backspace')
                    pyautogui.press('backspace')
                    for y in range(len(next_world_name)):
                        pyautogui.press('backspace')
                    time.sleep(0.1)
                    pyautogui.typewrite(world_name)
                    pyautogui.press('enter')

                    # Wait for the world to load before capturing the screenshot
                    time.sleep(3)  # Adjust the duration based on the world loading time

                    # Capture the whole screen
                    screenshot = pyautogui.screenshot()

                    # Convert the screenshot to a NumPy array
                    unseen_image = np.array(screenshot)

                    # Use pytesseract to extract text from the specific area of the screen
                    extracted_text1 = ocr_screen_text()

                    time.sleep(1)

                    # Capture the whole screen
                    screenshot = pyautogui.screenshot()

                    # Convert the screenshot to a NumPy array
                    unseen_image = np.array(screenshot)

                    # Use pytesseract to extract text from the specific area of the screen
                    extracted_text2 = ocr_screen_text()

                    time.sleep(1)

                    # Capture the whole screen
                    screenshot = pyautogui.screenshot()

                    # Convert the screenshot to a NumPy array
                    unseen_image = np.array(screenshot)

                    # Use pytesseract to extract text from the specific area of the screen
                    extracted_text3 = ocr_screen_text()

                    extracted_text = extracted_text3 + extracted_text2 + extracted_text1

                    # If the extracted text contains "World Locked by," report the world as taken (Class 1)
                    if "locked" in extracted_text or "Locked" in extracted_text:
                        predicted_class = 1
                    else:
                        predicted_class = 0

                    pyautogui.click(2443, 117)
                    time.sleep(0.2)
                    pyautogui.click(1328, 252)
                    time.sleep(0.1)

                    # If the world is not taken (Class 0) or locked, save the last world name to the text file
                    if predicted_class == 0 and last_world_name is not None:
                        updated_worlds.append(world_name)

        # Update the "unseen_worlds.txt" file with the non-locked worlds
        with open("unseen_worlds.txt", "w") as file:
            file.writelines(updated_worlds)

    def error_message(self, message):
        error_window = tk.Toplevel(self.master)
        error_window.title("Error")
        error_label = tk.Label(error_window, text=message)
        error_label.pack(side="top")
        error_button = tk.Button(error_window, text="OK", command=error_window.destroy)
        error_button.pack(side="bottom")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Growtopia World Finder v2.4")
    app = App(master=root)
    app.mainloop()
