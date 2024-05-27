from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from datetime import datetime
import json

# json setup for saving settings prefereences
def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f)

class RoutineManager:
    def __init__(self, root, desstop):
        self.root = root
        self.desstop = desstop
        self.routines = self.desstop.settings.get("routines", {})
    
    # opens routine setup window
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

    # setup options
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
        self.desstop.settings["routines"] = self.routines
        save_settings(self.desstop.settings)
        messagebox.showinfo("Success", f"Routine '{name}' saved successfully")
        self.routine_window.destroy()

    # manually activate routine
    def execute_routine(self, name):
        routine = self.routines.get(name)
        if routine:
            commands = routine["commands"]
            for command in commands:
                self.desstop.process_custom_command(command)
        else:
            self.desstop.terminal_output.insert(tk.END, f"Routine '{name}' not found\n")
            self.desstop.update_dess("surprised")

    # time activate routine
    def schedule_routines(self):
        now = datetime.now().strftime("%H:%M:%S")
        for name, routine in self.routines.items():
            routine_time = routine.get("time")
            if routine_time and routine_time == now:
                self.execute_routine(name)