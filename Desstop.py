import tkinter as tk
from tkinter import scrolledtext, messagebox
from threading import Thread
import subprocess
import time
from datetime import datetime
import random
import keyboard
import pyautogui

class Desstop:
    def __init__(self, root):
        self.root = root
        self.root.title("Desstop")
        
        self.dess_label = tk.Label(root, text="(•‿•)", font=("Arial", 24))
        self.dess_label.pack(pady=20)
        
        self.command_window = tk.Toplevel(root)
        self.command_window.title("Terminal")
        
        self.terminal_input = tk.Entry(self.command_window, width=50)
        self.terminal_input.pack(pady=10)
        self.terminal_input.bind("<Return>", self.process_command)
        initial_x_offset = 300 
        initial_y_offset = 100  
        self.command_window.geometry(f"+{initial_x_offset}+{initial_y_offset}")
        
        self.terminal_output = scrolledtext.ScrolledText(self.command_window, width=60, height=15)
        self.terminal_output.pack(pady=10)
        
        #If you want to add more faces, add them here. Seperate them by adding a comma at the end of the line
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
        
        self.wheel_outcomes = ["Outcome 1", "Outcome 2", "Outcome 3"]
        self.program_paths = {
            "example": r"C:\example\example\example.exe",
        }

        #If you want to add more commands, do so by adding them here first. Seperated by comma
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

    def move_windows_to_top(self):
        mouse_x, mouse_y = pyautogui.position()

        offset_x = -150 
        offset_y = -50  

        new_x = mouse_x + offset_x
        new_y = mouse_y + offset_y
        self.command_window.geometry(f"+{new_x}+{new_y}")

        self.command_window.attributes('-topmost', True)
        self.root.attributes('-topmost', True)

        self.terminal_input.focus_set()

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
        messagebox.showinfo("Settings", "Wheel outcomes saved successfully!")

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
        messagebox.showinfo("Settings", "Program paths saved successfully!")

    def process_command(self, event):
        command = self.terminal_input.get()
        self.terminal_input.delete(0, tk.END)

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

    #Add functionality for your command around here

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

        animate_spin()

    def start_countdown(self, duration_str):
        try:
            duration = self.parse_duration(duration_str)
            if duration:
                self.countdown_window = tk.Toplevel(self.root)
                self.countdown_window.title("Countdown")
                self.countdown_label = tk.Label(self.countdown_window, text="", font=("Arial", 24))
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

    def blink(self):
        self.update_dess("blink")
        self.root.after(200, lambda: self.update_dess("default"))

    def sleep(self):
        self.awake = False
        self.update_dess("sleep")

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

    #Add your command to the list
    def show_commands(self):
        commands = """
        Commands:
        - open {program}
        - time
        - settings
        - spin {wheelname}
        - blink
        - sleep
        - awake
        - thanks, {Desstop, Dess, DT}
        - list
        - countdown {0s, 0m, 0h} 
        """
        self.terminal_output.insert(tk.END, commands + "\n")
        self.update_dess("happy")

    def update_dess(self, face):
        self.dess_label.config(text=self.ascii_faces.get(face, "(•‿•)"))

if __name__ == "__main__":
    root = tk.Tk()
    app = Desstop(root)
    root.mainloop()
