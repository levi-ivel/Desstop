import tkinter as tk
from tkinter import scrolledtext, messagebox
from threading import Thread
import subprocess
import time
from datetime import datetime
import random
import keyboard
import pyautogui
import json

# Function to save settings to a JSON file
def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f)

# Function to load settings from a JSON file
def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default settings if file doesn't exist
        return {
            "wheel_outcomes": ["Outcome 1", "Outcome 2", "Outcome 3"],
            "program_paths": {
                "example": r"C:\example\example\example.exe",
            }
        }

class Desstop:
    def __init__(self, root):
        self.root = root
        self.root.title("Desstop")

        self.settings = load_settings()
        self.wheel_outcomes = self.settings.get("wheel_outcomes", ["Outcome 1", "Outcome 2", "Outcome 3"])
        self.program_paths = self.settings.get("program_paths", {"example": r"C:\example\example\example.exe"})

        self.dess_label = tk.Label(root, text="(•‿•)", font=("Arial", 24))
        self.dess_label.pack(pady=20)

        self.command_window = tk.Toplevel(root)
        self.command_window.title("Terminal")

        self.terminal_input_cmd = tk.Entry(self.command_window, width=50)
        self.terminal_input_cmd.pack(pady=10)
        self.terminal_input_cmd.bind("<Return>", self.process_command)
        initial_x_offset = 300
        initial_y_offset = 100
        self.command_window.geometry(f"+{initial_x_offset}+{initial_y_offset}")

        self.terminal_output = scrolledtext.ScrolledText(self.command_window, width=60, height=15)
        self.terminal_output.pack(pady=10)

        # ASCII faces for different states
        self.ascii_faces = {
            "default": "(•‿•)",
            "happy": "(•◡•)",
            "surprised": "(⊙_☉)",
            "blink": "(^_^)",
            "sleep": "(─‿─) zzz...",
            "irritated": "(≖_≖)",
            "thanks": "(^_^)b",
            "working": "(ง •̀_•́)ง",
            "scream": "'\(·`囗´· ｡)՞'"
        }
        self.awake = True
        self.terminal_output.insert(tk.END, "Hello, I'm Desstop! Please use commands list and settings to get started! \n You can call this window at any time by pressing CTRL + D \n whilst the program is running.\n")

        keyboard.add_hotkey('ctrl+d', self.move_windows_to_top)

        # Command dictionary
        self.commands = {
            "open": self.open_program,
            "time": self.say_time,
            "settings": self.show_settings,
            "spin": self.spin_wheel,
            "blink": self.blink,
            "sleep": self.sleep,
            "awake": self.awake_,
            "thanks": self.thanks,
            "list": self.show_commands,
            "countdown": self.start_countdown
        }

    def process_command(self, event):
        command = self.terminal_input_cmd.get()
        self.terminal_input_cmd.delete(0, tk.END)
        self.terminal_output.insert(tk.END, f"> {command}\n")

        if not self.awake and command not in ["awake", "list"]:
            self.terminal_output.insert(tk.END, "zzz...\n")
            return

        parts = command.split()
        main_command = parts[0].lower()

        if main_command in self.commands:
            self.commands[main_command](*parts[1:])
        else:
            self.terminal_output.insert(tk.END, f"Unknown command: {command}\n")
            self.update_dess("surprised")

    def move_windows_to_top(self):
        mouse_x, mouse_y = pyautogui.position()
        offset_x = -150
        offset_y = -50

        new_x = mouse_x + offset_x
        new_y = mouse_y + offset_y
        self.command_window.geometry(f"+{new_x}+{new_y}")

        self.command_window.attributes('-topmost', True)
        self.root.attributes('-topmost', True)

        self.terminal_input_cmd.focus_set()

        self.command_window.after(100, lambda: self.command_window.attributes('-topmost', False))
        self.root.after(100, lambda: self.root.attributes('-topmost', False))

        self.dess_label.lift()
        self.command_window.lift()

    def show_settings(self):
        self.terminal_output.insert(tk.END, "Opening settings windows...\n")
        self.update_dess("working")

        wheel_settings_window = tk.Toplevel(self.root)
        wheel_settings_window.title("Set Wheel Outcomes")

        wheel_label = tk.Label(wheel_settings_window, text="Wheel Outcomes:", font=("Arial", 14))
        wheel_label.pack(pady=10)

        self.wheel_outcomes_entry = scrolledtext.ScrolledText(wheel_settings_window, width=40, height=10)
        self.wheel_outcomes_entry.pack(pady=10)
        self.wheel_outcomes_entry.insert(tk.END, "\n".join(self.wheel_outcomes))

        save_wheel_outcomes_button = tk.Button(wheel_settings_window, text="Save", command=self.save_wheel_outcomes)
        save_wheel_outcomes_button.pack(pady=10)

        program_settings_window = tk.Toplevel(self.root)
        program_settings_window.title("Set Program Paths")

        program_label = tk.Label(program_settings_window, text="Program Paths:", font=("Arial", 14))
        program_label.pack(pady=10)

        self.program_paths_text = scrolledtext.ScrolledText(program_settings_window, width=60, height=15)
        self.program_paths_text.pack(pady=10)
        self.load_program_paths()

        save_program_paths_button = tk.Button(program_settings_window, text="Save", command=self.save_program_paths)
        save_program_paths_button.pack(pady=10)

    def save_wheel_outcomes(self):
        outcomes_text = self.wheel_outcomes_entry.get("1.0", tk.END).strip()
        self.wheel_outcomes = outcomes_text.split("\n")
        self.settings["wheel_outcomes"] = self.wheel_outcomes
        save_settings(self.settings)
        self.terminal_output.insert(tk.END, "Wheel outcomes saved successfully!\n")
        self.update_dess("happy")

    def load_program_paths(self):
        paths_text = "\n".join([f"{name}: {path}" for name, path in self.program_paths.items()])
        self.program_paths_text.insert(tk.END, paths_text)

    def save_program_paths(self):
        paths_text = self.program_paths_text.get("1.0", tk.END).strip()
        new_program_paths = {}
        for line in paths_text.split("\n"):
            if ": " in line:
                name, path = line.split(": ", 1)
                new_program_paths[name.lower()] = path
        self.program_paths = new_program_paths
        self.settings["program_paths"] = self.program_paths
        save_settings(self.settings)
        self.terminal_output.insert(tk.END, "Program paths saved successfully!\n")
        self.update_dess("happy")

    def open_program(self, program_name):
        try:
            program_path = self.program_paths.get(program_name.lower())
            if program_path:
                subprocess.Popen([program_path])
                self.terminal_output.insert(tk.END, f"Opening {program_name}...\n")
                self.update_dess("happy")
            else:
                self.terminal_output.insert(tk.END, f"Unknown program: {program_name}\n")
                self.update_dess("surprised")
        except Exception as e:
            self.terminal_output.insert(tk.END, f"Failed to open {program_name}: {str(e)}\n")
            self.update_dess("surprised")

    def say_time(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.terminal_output.insert(tk.END, f"The current time is {now}\n")
        self.update_dess("happy")

    def spin_wheel(self, wheelname):
        wheel_window = tk.Toplevel(self.root)
        wheel_window.title(f"Spinning {wheelname} Wheel")
        wheel_label = tk.Label(wheel_window, text="", font=("Arial", 24))
        wheel_label.pack(pady=20)

        def animate_spin():
            for _ in range(30):
                result = random.choice(self.wheel_outcomes)
                wheel_label.config(text=result)
                wheel_window.update()
                time.sleep(0.05)
            self.terminal_output.insert(tk.END, f"The wheel landed on: {result}\n")
            self.update_dess("happy")

        spin_thread = Thread(target=animate_spin)
        spin_thread.start()

    def blink(self):
        self.update_dess("blink")
        self.terminal_output.insert(tk.END, "Blink!\n")

    def sleep(self):
        self.awake = False
        self.update_dess("sleep")
        self.terminal_output.insert(tk.END, "Going to sleep...\n")

    def awake_(self):
        self.awake = True
        self.update_dess("default")
        self.terminal_output.insert(tk.END, "I'm awake!\n")

    def thanks(self):
        self.update_dess("thanks")
        self.terminal_output.insert(tk.END, "Thank you!\n")

    def show_commands(self):
        self.terminal_output.insert(tk.END, "Available commands: open, time, settings, spin, blink, sleep, awake, thanks, list, countdown\n")
        self.update_dess("default")

    def start_countdown(self, seconds):
        try:
            seconds = int(seconds)
            self.terminal_output.insert(tk.END, f"Starting countdown for {seconds} seconds...\n")
            self.update_dess("working")
            countdown_thread = Thread(target=self.countdown, args=(seconds,))
            countdown_thread.start()
        except ValueError:
            self.terminal_output.insert(tk.END, "Please provide a valid number of seconds for the countdown.\n")
            self.update_dess("irritated")

    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            self.terminal_output.insert(tk.END, f"{i}...\n")
            self.terminal_output.yview(tk.END)
            time.sleep(1)
        self.terminal_output.insert(tk.END, "Time's up!\n")
        self.update_dess("happy")

    def update_dess(self, state):
        self.dess_label.config(text=self.ascii_faces.get(state, "(•‿•)"))

if __name__ == "__main__":
    root = tk.Tk()
    app = Desstop(root)
    root.mainloop()
