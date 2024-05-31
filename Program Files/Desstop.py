from tkinter import scrolledtext, messagebox, ttk, colorchooser
from threading import Thread
from datetime import datetime
import tkinter as tk
import subprocess
import time
import keyboard
import pyautogui
import json
import random

#START --json--
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
            "routines": {},
            "keybind": "ctrl+d",
            "colors": {
                "face_color": "#2ecc71",
                "background_color": "#34495e",
                "text_field_color": "#2c3e50",
                "text_color": "white"
            }
        }
#END --json--

#START --setup--
class Desstop:
    def __init__(self, root):
        self.root = root
        self.settings = load_settings()
        self.keybind = self.settings.get("keybind", "ctrl+d")
        self.colors = self.settings.get("colors", {
            "face_color": "#2ecc71",
            "background_color": "#34495e",
            "text_field_color": "#2c3e50",
            "text_color": "white"
        })
        
        self.root.title("Desstop")
        self.root.configure(bg=self.colors["background_color"])

        self.settings = load_settings()
        self.routines = self.settings.get("routines", {})
        self.wheel_outcomes = self.settings.get("wheel_outcomes", ["Outcome 1", "Outcome 2", "Outcome 3"])
        self.program_paths = self.settings.get("program_paths", {"example": r"C:\example\example\example.exe"})

        self.dess_label = tk.Label(root, text="(•‿•)", font=("Helvetica", 24), fg=self.colors["face_color"], bg=self.colors["background_color"])
        self.dess_label.pack(pady=20)

        self.command_window = tk.Toplevel(root)
        self.command_window.title("Terminal")
        self.command_window.configure(bg=self.colors["background_color"])

        self.terminal_input_cmd = tk.Entry(self.command_window, width=50, font=("Helvetica", 12), bg=self.colors["text_field_color"], fg=self.colors["text_color"], insertbackground=self.colors["text_color"]) 
        self.terminal_input_cmd.pack(pady=10)
        self.terminal_input_cmd.bind("<Return>", self.process_command)
        initial_x_offset = 300
        initial_y_offset = 100
        self.command_window.geometry(f"+{initial_x_offset}+{initial_y_offset}")

        self.terminal_output = scrolledtext.ScrolledText(self.command_window, width=60, height=15, font=("Helvetica", 10), bg=self.colors["text_field_color"], fg=self.colors["text_color"]) 
        self.terminal_output.pack(pady=10)

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
        self.terminal_output.insert(tk.END, f"Hello, I'm Desstop! \n Please use the commands list and settings to get started! \n You can call this window at any time by pressing {self.keybind} \n whilst the program is running.\n")

        keyboard.add_hotkey(self.keybind, self.move_windows_to_top)

        self.check_routines()
#END --setup--

#START --utility--
    # process and execute command
    def process_command(self, event):
        command = self.terminal_input_cmd.get()
        self.terminal_input_cmd.delete(0, tk.END)
        self.terminal_output.insert(tk.END, f"> {command}\n")

        if not self.awake and command not in ["awake ", "list"]:
            self.terminal_output.insert(tk.END, "zzz...\n")
            return

        parts = command.split()
        main_command = parts[0].lower()

        if main_command in self.commands:
            self.commands[main_command](*parts[1:])
        elif main_command == "routine":
            if len(parts) == 3 and parts[2].lower() == "edit":
                routine_name = parts[1]
                self.open_routine_window(routine_name)
            else:
                routine_name = " ".join(parts[1:])
                self.execute_routine(routine_name)
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
#END --utility--

#START --settings--
    # open the wheel and program setting windows
    def show_settings(self):
        self.terminal_output.insert(tk.END, "Opening settings windows...\n")
        self.update_dess("working")
        
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.configure(bg=self.colors["background_color"]) 

        # Create a frame to contain the settings
        settings_frame = tk.Frame(settings_window, bg=self.colors["background_color"])
        settings_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas to hold the settings frame
        settings_canvas = tk.Canvas(settings_frame, bg=self.colors["background_color"])
        settings_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        settings_scrollbar = tk.Scrollbar(settings_frame, orient=tk.VERTICAL, command=settings_canvas.yview)
        settings_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        settings_canvas.configure(yscrollcommand=settings_scrollbar.set)
        settings_canvas.bind('<Configure>', lambda e: settings_canvas.configure(scrollregion=settings_canvas.bbox("all")))

        scrollable_frame = tk.Frame(settings_canvas, bg=self.colors["background_color"])
        settings_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Wheel Outcomes Section
        wheel_label = tk.Label(scrollable_frame, text="Wheel Outcomes:", font=("Helvetica", 14), bg=self.colors["background_color"], fg=self.colors["text_color"]) 
        wheel_label.pack(pady=10)

        self.wheel_outcomes_entry = scrolledtext.ScrolledText(scrollable_frame, width=60, height=15, font=("Helvetica", 10), bg=self.colors["text_field_color"], fg=self.colors["text_color"]) 
        self.wheel_outcomes_entry.pack(pady=10)
        self.wheel_outcomes_entry.insert(tk.END, "\n".join(self.wheel_outcomes))

        save_wheel_outcomes_button = tk.Button(scrollable_frame, text="Save Wheel Outcomes", command=self.save_wheel_outcomes, bg="#2ecc71", fg=self.colors["text_color"]) 
        save_wheel_outcomes_button.pack(pady=10)

        # Program Paths Section
        program_label = tk.Label(scrollable_frame, text="Program Paths:", font=("Arial", 14), bg=self.colors["background_color"], fg=self.colors["text_color"])
        program_label.pack(pady=10)

        self.program_paths_text = scrolledtext.ScrolledText(scrollable_frame, width=60, height=15, font=("Helvetica", 10), bg=self.colors["text_field_color"], fg=self.colors["text_color"]) 
        self.program_paths_text.pack(pady=10)
        self.load_program_paths()

        save_program_paths_button = tk.Button(scrollable_frame, text="Save Program Paths", command=self.save_program_paths, bg="#2ecc71", fg=self.colors["text_color"]) 
        save_program_paths_button.pack(pady=10)

        # General Settings Section
        general_settings_label = tk.Label(scrollable_frame, text="General Settings", font=("Arial", 14), bg=self.colors["background_color"], fg=self.colors["text_color"])
        general_settings_label.pack(pady=10)

        keybind_label = tk.Label(scrollable_frame, text="Keybind:", font=("Helvetica", 14), bg=self.colors["background_color"], fg=self.colors["text_color"]) 
        keybind_label.pack(pady=10)

        self.keybind_entry = tk.Entry(scrollable_frame, width=20, font=("Helvetica", 12), bg=self.colors["text_field_color"], fg=self.colors["text_color"], insertbackground=self.colors["text_color"]) 
        self.keybind_entry.pack(pady=10)
        self.keybind_entry.insert(tk.END, self.keybind)

        face_color_label = tk.Label(scrollable_frame, text="Face Color:", font=("Helvetica", 14), bg=self.colors["background_color"], fg=self.colors["text_color"]) 
        face_color_label.pack(pady=10)

        self.face_color_button = tk.Button(scrollable_frame, text="Choose Face Color", command=self.choose_face_color, bg=self.colors["face_color"], fg=self.colors["text_color"])
        self.face_color_button.pack(pady=10)

        background_color_label = tk.Label(scrollable_frame, text="Background Color:", font=("Helvetica", 14), bg=self.colors["background_color"], fg=self.colors["text_color"]) 
        background_color_label.pack(pady=10)

        self.background_color_button = tk.Button(scrollable_frame, text="Choose Background Color", command=self.choose_background_color, bg=self.colors["background_color"], fg=self.colors["text_color"])
        self.background_color_button.pack(pady=10)

        text_field_color_label = tk.Label(scrollable_frame, text="Text Field Color:", font=("Helvetica", 14), bg=self.colors["background_color"], fg=self.colors["text_color"]) 
        text_field_color_label.pack(pady=10)

        self.text_field_color_button = tk.Button(scrollable_frame, text="Choose Text Field Color", command=self.choose_text_field_color, bg=self.colors["text_field_color"], fg=self.colors["text_color"])
        self.text_field_color_button.pack(pady=10)

        text_color_label = tk.Label(scrollable_frame, text="Text Color:", font=("Helvetica", 14), bg=self.colors["background_color"], fg=self.colors["text_color"]) 
        text_color_label.pack(pady=10)

        self.text_color_button = tk.Button(scrollable_frame, text="Choose Text Color", command=self.choose_text_color, bg=self.colors["text_color"], fg=self.colors["background_color"])
        self.text_color_button.pack(pady=10)

        save_general_settings_button = tk.Button(scrollable_frame, text="Save General Settings", command=self.save_general_settings, bg="#2ecc71", fg=self.colors["text_color"]) 
        save_general_settings_button.pack(pady=10)
        
        reset_colors_button = tk.Button(scrollable_frame, text="Reset to Color Default", command=self.reset_colors_to_default, bg="#3498db", fg=self.colors["text_color"]) 
        reset_colors_button.pack(pady=10)

        
    def choose_face_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.colors["face_color"] = color
            self.face_color_button.configure(bg=color)

    def choose_background_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.colors["background_color"] = color
            self.root.configure(bg=color)
            self.command_window.configure(bg=color)
            self.face_color_button.configure(bg=color)
            self.background_color_button.configure(bg=color)
            self.text_field_color_button.configure(bg=color)
            self.text_color_button.configure(bg=color)

    def choose_text_field_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.colors["text_field_color"] = color
            self.terminal_input_cmd.configure(bg=color)
            self.terminal_output.configure(bg=color)

    def choose_text_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.colors["text_color"] = color
            self.terminal_input_cmd.configure(fg=color, insertbackground=color)
            self.terminal_output.configure(fg=color)

    def reset_colors_to_default(self):
        default_colors = {
            "face_color": "#2ecc71",
            "background_color": "#34495e",
            "text_field_color": "#2c3e50",
            "text_color": "white"
        }
        self.colors = default_colors

        # Update UI elements with default colors
        self.root.configure(bg=default_colors["background_color"])
        self.command_window.configure(bg=default_colors["background_color"])
        self.face_color_button.configure(bg=default_colors["face_color"])
        self.background_color_button.configure(bg=default_colors["background_color"])
        self.text_field_color_button.configure(bg=default_colors["text_field_color"])
        self.text_color_button.configure(bg=default_colors["text_color"])

        # Update settings and save
        self.settings["colors"] = default_colors
        save_settings(self.settings)
        self.terminal_output.insert(tk.END, "Colors reset to default.\n")


    # save settings to json
    def save_general_settings(self):
        self.keybind = self.keybind_entry.get()
        self.settings["keybind"] = self.keybind
        self.settings["colors"] = self.colors
        save_settings(self.settings)
        try:
            keyboard.remove_hotkey(self.keybind)
        except:
            pass
        keyboard.add_hotkey(self.keybind, self.move_windows_to_top)
        self.terminal_output.insert(tk.END, "General settings saved successfully!\n")
        self.update_dess("happy")
    
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
#END --settings--

#START --commands--

#START --main commands--
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

    def show_commands(self):
        self.terminal_output.insert(tk.END, "Available commands: open {program},\n time,\n settings,\n spin {wheelname},\n blink,\n sleep,\n awake,\n thanks {desstop, dess, dt},\n list,\n countdown {0s, 0m, 0h},\n routine,\n routine {routinename)\n, routine {routinename} edit\n ")
        self.update_dess("default")

    def say_time(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.terminal_output.insert(tk.END, f"The current time is {now}\n")
        self.update_dess("happy")

#START --countdown--
    def start_countdown(self, *duration_args):
        try:
            total_seconds = 0
            for duration_arg in duration_args:
                duration_str = duration_arg.lower()
                value = int(duration_str[:-1])
                unit = duration_str[-1]
                if unit == 's':
                    total_seconds += value
                elif unit == 'm':
                    total_seconds += value * 60
                elif unit == 'h':
                    total_seconds += value * 3600
                else:
                    raise ValueError(f"Invalid duration format: {duration_arg}")
            if total_seconds <= 0:
                raise ValueError("Duration must be greater than zero")

            self.countdown_window = tk.Toplevel(self.root)
            self.countdown_window.title("Countdown")
            self.countdown_window.configure(bg="#34495e")
            self.countdown_label = tk.Label(self.countdown_window, text="", font=("Helvetica", 24), bg="#34495e", fg="white")
            self.countdown_label.pack(pady=20)
            Thread(target=self.run_countdown, args=(total_seconds,)).start()
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
#END --countdown--

#START -wheel--
    def spin_wheel(self, wheelname):
        wheel_window = tk.Toplevel(self.root)
        wheel_window.title(f"Spinning {wheelname} Wheel")
        wheel_window.configure(bg="#34495e") 
        wheel_label = tk.Label(wheel_window, text="", font=("Helvetica", 24), bg="#34495e", fg="white")
        wheel_label.pack(pady=20)

        def animate_spin():
            for _ in range(30):
                result = random.choice(self.settings["wheel_outcomes"])
                wheel_label.config(text=result)
                wheel_window.update()
                time.sleep(0.05)
            self.terminal_output.insert(tk.END, f"The wheel landed on: {result}\n")
            self.update_dess("happy")

        spin_thread = Thread(target=animate_spin)
        spin_thread.start()
#END --wheel--

#START --routines--
    def manage_routine(self, *args):
        if len(args) == 1:
            routine_name = args[0]
            self.execute_routine(routine_name)
        elif len(args) == 2 and args[1].lower() == "edit":
            routine_name = args[0]
            self.open_routine_window(routine_name)
        else:
            self.open_routine_window()

    def check_routines(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.schedule_routines()
        self.root.after(1000, self.check_routines)

    def process_custom_command(self, command):
            parts = command.split()
            main_command = parts[0].lower()
    
            if main_command in self.commands:
                self.commands[main_command](*parts[1:])
            elif main_command == "routine":
                if len(parts) == 3 and parts[2].lower() == "edit":
                    routine_name = parts[1]
                    self.open_routine_window(routine_name)
                else:
                    routine_name = " ".join(parts[1:])
                    self.execute_routine(routine_name)
            else:
                self.terminal_output.insert(tk.END, f"Unknown command: {command}\n")
                self.update_dess("surprised")

    # setup and initialize routine window
    def open_routine_window(self, routine_name=None):
        self.routine_window = tk.Toplevel(self.root)
        self.routine_window.title("Routine Manager")
        self.routine_window.configure(bg="#34495e") 

        self.routine_name_var = tk.StringVar(value=routine_name)
        self.command_var = tk.StringVar()
        self.time_var = tk.StringVar()

        ttk.Label(self.routine_window, text="Routine Name:", background="#34495e", foreground="white").pack(pady=5) 
        tk.Entry(self.routine_window, background="#34495e", foreground="white", textvariable=self.routine_name_var).pack(pady=5)

        ttk.Label(self.routine_window, text="Command:", background="#34495e", foreground="white").pack(pady=5) 
        tk.Entry(self.routine_window, background="#34495e", foreground="white", textvariable=self.command_var).pack(pady=5)

        ttk.Label(self.routine_window, text="Time (optional, format HH:MM:SS):", background="#34495e", foreground="white").pack(pady=5) 
        tk.Entry(self.routine_window, background="#34495e", foreground="white", textvariable=self.time_var).pack(pady=5)

        tk.Button(self.routine_window, text="Add Command", command=self.add_command, bg="#2ecc71", fg="white").pack(pady=5)
        tk.Button(self.routine_window, text="Save Routine", command=self.save_routine, bg="#2ecc71", fg="white").pack(pady=5) 

        self.command_listbox = tk.Listbox(self.routine_window, bg="#34495e", fg="white")
        self.command_listbox.pack(pady=5, fill=tk.BOTH, expand=True)

        tk.Button(self.routine_window, text="Remove Selected Command", command=self.remove_command, bg="#e74c3c", fg="white").pack(pady=5) 

        if routine_name and routine_name in self.routines:
            routine = self.routines[routine_name]
            self.time_var.set(routine.get("time", ""))
            for command in routine.get("commands", []):
                self.command_listbox.insert(tk.END, command)

    def add_command(self):
        command = self.command_var.get().strip()
        if command:
            self.command_listbox.insert(tk.END, command)
            self.command_var.set("")
        else:
            messagebox.showerror("Error", "Command cannot be empty")

    def remove_command(self):
        selected = self.command_listbox.curselection()
        if selected:
            self.command_listbox.delete(selected)

    def save_routine(self):
        name = self.routine_name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Routine name cannot be empty")
            return

        commands = self.command_listbox.get(0, tk.END)
        if not commands:
            messagebox.showerror("Error", "Routine must have at least one command")
            return

        routine = {
            "commands": list(commands),
            "time": self.time_var.get().strip() or None
        }
        self.routines[name] = routine
        self.settings["routines"] = self.routines
        save_settings(self.settings)
        messagebox.showinfo("Success", f"Routine '{name}' saved successfully")
        self.routine_window.destroy()

    # manually activate routine
    def execute_routine(self, name):
        routine = self.routines.get(name)
        if routine:
            commands = routine["commands"]
            for command in commands:
                self.process_custom_command(command)
        else:
            self.terminal_output.insert(tk.END, f"Routine '{name}' not found\n")
            self.update_dess("surprised")

    # time activate routine
    def schedule_routines(self):
        now = datetime.now().strftime("%H:%M:%S")
        for name, routine in self.routines.items():
            routine_time = routine.get("time")
            if routine_time and routine_time == now:
                self.execute_routine(name)
#END --routines--

#END --main commands--

#START --for fun commands--
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
#END --for fun commands--

#END --commands--

    def update_dess(self, state):
        self.dess_label.config(text=self.ascii_faces.get(state, "(•‿•)"))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Desstop")
    root.configure(bg="#34495e") 

    app = Desstop(root)

    root.mainloop()

