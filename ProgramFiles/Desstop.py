import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import subprocess
import time
from datetime import datetime
import random
import keyboard
import pyautogui
import json
from RoutineManager import RoutineManager

# json setup for saving/loading setting preferences
def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f)

def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "wheel_outcomes": ["Outcome 1", "Outcome 2", "Outcome 3"],
            "program_paths": {
                "example": r"C:\example\example\example.exe",
            },
            "routines": {}
        }

class Desstop:

    # setup and initialize face and terminal window
    def __init__(self, root):
        self.root = root
        self.root.title("Desstop")
        self.root.configure(bg="#34495e")

        self.settings = load_settings()
        self.wheel_outcomes = self.settings.get("wheel_outcomes", ["Outcome 1", "Outcome 2", "Outcome 3"])
        self.program_paths = self.settings.get("program_paths", {"example": r"C:\example\example\example.exe"})
        self.routine_manager = RoutineManager(self.root, self)

        self.dess_label = tk.Label(root, text="(•‿•)", font=("Helvetica", 24), fg="#2ecc71", bg="#34495e")
        self.dess_label.pack(pady=20)

        self.command_window = tk.Toplevel(root)
        self.command_window.title("Terminal")
        self.command_window.configure(bg="#34495e")

        self.terminal_input_cmd = tk.Entry(self.command_window, width=50, font=("Helvetica", 12), bg="#2c3e50", fg="white", insertbackground="white") 
        self.terminal_input_cmd.pack(pady=10)
        self.terminal_input_cmd.bind("<Return>", self.process_command)
        initial_x_offset = 300
        initial_y_offset = 100
        self.command_window.geometry(f"+{initial_x_offset}+{initial_y_offset}")

        self.terminal_output = scrolledtext.ScrolledText(self.command_window, width=60, height=15, font=("Helvetica", 10), bg="#2c3e50", fg="white") 
        self.terminal_output.pack(pady=10)

        # list available faces
        self.ascii_faces = {
            "default": "(•‿•)",
            "happy": "(•◡•)",
            "surprised": "(⊙_☉)",
            "blink": "(^_^)",
            "sleep": "(─‿─) zzz...",
            "irritated": "(≖_≖)",
            "thanks": "(^_^)b",
            "working": "(ง •̀_•́)ง",
            "scream": "｡゜(｀Д´)゜｡"
        }

        # list available commands
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
            "countdown": self.start_countdown,
            "routine": self.manage_routine
        }

        self.awake = True
        self.terminal_output.insert(tk.END, "Hello, I'm Desstop! \n Please use commands list and settings to get started! \n You can call this window at any time by pressing CTRL + D \n whilst the program is running.\n")

        keyboard.add_hotkey('ctrl+d', self.move_windows_to_top)

        self.check_routines()

    # process and execute command
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
        elif main_command == "routine":
            if len(parts) == 3 and parts[2].lower() == "edit":
                routine_name = parts[1]
                self.routine_manager.open_routine_window(routine_name)
            else:
                routine_name = " ".join(parts[1:])
                self.routine_manager.execute_routine(routine_name)
        else:
            self.terminal_output.insert(tk.END, f"Unknown command: {command}\n")
            self.update_dess("surprised")

    # move windows to front upon keybind press
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

    # open the wheel and program setting windows 
    def show_settings(self):
        self.terminal_output.insert(tk.END, "Opening settings windows...\n")
        self.update_dess("working")

        wheel_settings_window = tk.Toplevel(self.root)
        wheel_settings_window.title("Set Wheel Outcomes")
        wheel_settings_window.configure(bg="#34495e") 

        wheel_label = tk.Label(wheel_settings_window, text="Wheel Outcomes:", font=("Helvetica", 14), bg="#34495e", fg="white") 
        wheel_label.pack(pady=10)

        self.wheel_outcomes_entry = scrolledtext.ScrolledText(wheel_settings_window, width=60, height=15, font=("Helvetica", 10), bg="#2c3e50", fg="white") 
        self.wheel_outcomes_entry.pack(pady=10)
        self.wheel_outcomes_entry.insert(tk.END, "\n".join(self.wheel_outcomes))

        save_wheel_outcomes_button = tk.Button(wheel_settings_window, text="Save", command=self.save_wheel_outcomes, bg="#2ecc71", fg="white") 
        save_wheel_outcomes_button.pack(pady=10)

        program_settings_window = tk.Toplevel(self.root)
        program_settings_window.title("Set Program Paths")
        program_settings_window.configure(bg="#34495e") 

        program_label = tk.Label(program_settings_window, text="Program Paths:", font=("Arial", 14), bg="#34495e", fg="white")
        program_label.pack(pady=10)

        self.program_paths_text = scrolledtext.ScrolledText(program_settings_window, width=60, height=15, font=("Helvetica", 10), bg="#2c3e50", fg="white") 
        self.program_paths_text.pack(pady=10)
        self.load_program_paths()

        save_program_paths_button = tk.Button(program_settings_window, text="Save", command=self.save_program_paths, bg="#2ecc71", fg="white") 
        save_program_paths_button.pack(pady=10)
    
    # save settings to json
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

    # commands
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
        wheel_window.configure(bg="#34495e") 
        wheel_label = tk.Label(wheel_window, text="", font=("Helvetica", 24), bg="#34495e", fg="white")
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
        self.root.after(200, lambda: self.update_dess("default"))
        self.terminal_output.insert(tk.END, "Blink!\n")

    def sleep(self):
        self.awake = False
        self.update_dess("sleep")
        self.terminal_output.insert(tk.END, "Going to sleep...\n")

    def awake_(self):
        if self.awake:
            self.terminal_output.insert(tk.END, "I'm already awake.\n")
            self.update_dess("irritated")
        else:
            self.awake = True
            self.update_dess("default")
            self.terminal_output.insert(tk.END, "Zzz.... huh? Oh sorry, it appears I went to sleep.\n")

    def thanks(self, recipient):
        if recipient.lower() in ["desstop", "dess", "dt"]:
            self.terminal_output.insert(tk.END, "No problem!\n")
            self.update_dess("thanks")
        else:
            self.terminal_output.insert(tk.END, f"I'd like to hear my name, not {recipient}\n")
            self.update_dess("irritated")

    def show_commands(self):
        self.terminal_output.insert(tk.END, "Available commands: open {program},\n time,\n settings,\n spin {wheelname},\n blink,\n sleep,\n awake,\n thanks {desstop, dess, dt},\n list,\n countdown {0s, 0m, 0h},\n routine,\n routine {routinename)\n, routine {routinename} edit\n ")
        self.update_dess("default")

    def start_countdown(self, duration_str):
        try:
            duration = self.parse_duration(duration_str)
            if duration:
                self.countdown_window = tk.Toplevel(self.root)
                self.countdown_window.title("Countdown")
                self.countdown_window.configure(bg="#34495e") 
                self.countdown_label = tk.Label(self.countdown_window, text="", font=("Helvetica", 24), bg="#34495e", fg="white") 
                self.countdown_label.pack(pady=20)
                Thread(target=self.run_countdown, args=(duration,)).start()
            else:
                self.terminal_output.insert(tk.END, "Invalid duration format. Please use format like '10s', '5m', or '1h'\n")
                self.update_dess("surprised")
        except Exception as e:
            self.terminal_output.insert(tk.END, f"Error starting countdown: {str(e)}\n")
            self.update_dess("surprised")

    def parse_duration(self, duration_str):
        duration_str = duration_str.lower()
        total_seconds = 0
        parts = duration_str.split()
        for part in parts:
            value = int(part[:-1])
            unit = part[-1]
            if unit == 's':
                total_seconds += value
            elif unit == 'm':
                total_seconds += value * 60
            elif unit == 'h':
                total_seconds += value * 3600
            else:
                return None
        return total_seconds

    def run_countdown(self, duration):
        remaining_time = duration
        while remaining_time > 0:
            hours = remaining_time // 3600
            minutes = (remaining_time % 3600) // 60
            seconds = remaining_time % 60
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.countdown_label.config(text=time_str)
            self.countdown_window.update()
            time.sleep(1)
            remaining_time -= 1
        self.root.attributes('-topmost', True)
        self.command_window.after(100, lambda: self.command_window.attributes('-topmost', False))
        self.command_window.attributes('-topmost', True)
        self.root.after(100, lambda: self.root.attributes('-topmost', False))
        self.countdown_window.destroy()
        self.terminal_output.insert(tk.END, "Countdown finished!\n")
        self.update_dess("scream")
        self.root.after(4000, lambda: self.update_dess("working"))

    def manage_routine(self, *args):
        if len(args) == 1:
            routine_name = args[0]
            self.routine_manager.execute_routine(routine_name)
        elif len(args) == 2 and args[1].lower() == "edit":
            routine_name = args[0]
            self.routine_manager.open_routine_window(routine_name)
        else:
            self.routine_manager.open_routine_window()

    def check_routines(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.routine_manager.schedule_routines()
        self.root.after(1000, self.check_routines)

    def process_custom_command(self, command):
        parts = command.split()
        main_command = parts[0].lower()

        if main_command in self.commands:
            self.commands[main_command](*parts[1:])
        elif main_command == "routine":
            if len(parts) == 3 and parts[2].lower() == "edit":
                routine_name = parts[1]
                self.routine_manager.open_routine_window(routine_name)
            else:
                routine_name = " ".join(parts[1:])
                self.routine_manager.execute_routine(routine_name)
        else:
            self.terminal_output.insert(tk.END, f"Unknown command: {command}\n")
            self.update_dess("surprised")

    def update_dess(self, state):
        self.dess_label.config(text=self.ascii_faces.get(state, "(•‿•)"), bg="#34495e")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Desstop")
    root.configure(bg="#34495e") 

    app = Desstop(root)

    root.mainloop()
