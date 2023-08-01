import tkinter as tk
import pyautogui
import time
import random
import string
import keyboard

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.is_running = False

        # Bind pause key to stop_macro function
        keyboard.add_hotkey('pause', self.stop_macro)

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
            print("Warning: your selected number of iterations is greater than 100. This may lead to complications in search procedure.")
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
        self.is_running = True
        if self.is_running:
            pyautogui.click(1331, 279)
            for i in range(1, len(rand_list)):
                if not self.is_running:
                    break
                time.sleep(1)
                pyautogui.click(1331, 279)
                for y in range(len(rand_list[i])):
                    pyautogui.press('backspace')
                time.sleep(0.1)
                pyautogui.typewrite(rand_list[i])
                pyautogui.press('enter')
                time.sleep(2.5)
                pyautogui.click(1818, 107)
                time.sleep(0.2)
                pyautogui.click(960,187)
                time.sleep(0.1)

    def stop_macro(self):
        if self.is_running:
            self.is_running = False
        else:
            self.is_running = True
            self.run_macro(self.rand_list)

    def error_message(self, message):
        error_window = tk.Toplevel(self.master)
        error_window.title("Error")
        error_label = tk.Label(error_window, text=message)
        error_label.pack(side="top")
        error_button = tk.Button(error_window, text="OK", command=error_window.destroy)
        error_button.pack(side="bottom")

root = tk.Tk()
root.title("Growtopia World Finder v0.1")
app = App(master=root)
app.mainloop()
