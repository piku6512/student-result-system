"""
Student Result Management System - Simple Version
"""

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "students_data.json"

# Colors
BG = "#f0f0f0"
WHITE = "#ffffff"
BLUE = "#3498DB"
GREEN = "#27AE60"
RED = "#E74C3C"

class StudentSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result System")
        self.root.geometry("800x550")
        self.root.configure(bg=BG)
        
        self.students = {}
        self.load_data()
        self.show_main_menu()
    
    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                self.students = json.load(f)
    
    def save_data(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self.students, f, indent=4)
    
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()
    
    def show_main_menu(self):
        self.clear()
        
        # Title
        tk.Label(self.root, text="Student Result Management", 
            font=("Arial", 22, "bold"), bg=BG, fg=BLUE).pack(pady=20)
        
        # Menu Buttons
        btn_config = {"font": ("Arial", 14), "width": 20, "bg": BLUE, 
                      "fg": WHITE, "cursor": "hand2", "bd": 0}
        
        tk.Button(self.root, text="1. Add Student", command=self.add_student_screen, **btn_config).pack(pady=8)
        tk.Button(self.root, text="2. Enter Marks", command=self.marks_screen, **btn_config).pack(pady=8)
        tk.Button(self.root, text="3. View Results", command=self.results_screen, **btn_config).pack(pady=8)
        tk.Button(self.root, text="4. Delete Student", command=self.delete_student_screen, **btn_config).pack(pady=8)
        tk.Button(self.root, text="5. Exit", font=("Arial", 14), width=20, bg=RED, 
                  fg=WHITE, cursor="hand2", bd=0, command=self.root.quit).pack(pady=20)
    
    # ==================== ADD STUDENT ====================
    def add_student_screen(self):
        self.clear()
        
        tk.Label(self.root, text="Add New Student", font=("Arial", 18, "bold"), bg=BG).pack(pady=15)
        
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(pady=20)
        
        tk.Label(frame, text="Name:", font=("Arial", 12), bg=BG).grid(row=0, column=0, pady=5, sticky="w")
        name_entry = tk.Entry(frame, font=("Arial", 12), width=25)
        name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(frame, text="Class:", font=("Arial", 12), bg=BG).grid(row=1, column=0, pady=5, sticky="w")
        class_entry = tk.Entry(frame, font=("Arial", 12), width=25)
        class_entry.grid(row=1, column=1, pady=5, padx=5)
        
        def save():
            name = name_entry.get().strip()
            cls = class_entry.get().strip()
            
            if not name or not cls:
                messagebox.showerror("Error", "Fill all fields!")
                return
            
            # Generate ID
            sid = f"S{len(self.students) + 1:03d}"
            self.students[sid] = {"name": name, "class": cls, "marks": {}}
            self.save_data()
            messagebox.showinfo("Success", f"Student added! ID: {sid}")
            self.show_main_menu()
        
        tk.Button(self.root, text="Save", font=("Arial", 12), bg=GREEN, fg=WHITE,
            command=save).pack(pady=10)
        tk.Button(self.root, text="Back", font=("Arial", 11), command=self.show_main_menu).pack()
    
    # ==================== ENTER MARKS ====================
    def marks_screen(self):
        self.clear()
        
        if not self.students:
            tk.Label(self.root, text="No students! Add first.", font=("Arial", 14), bg=BG).pack(pady=50)
            tk.Button(self.root, text="Back", command=self.show_main_menu).pack()
            return
        
        tk.Label(self.root, text="Enter Marks", font=("Arial", 18, "bold"), bg=BG).pack(pady=15)
        
        # Select student
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(pady=10)
        
        tk.Label(frame, text="Select Student:", font=("Arial", 12), bg=BG).grid(row=0, column=0, pady=5)
        
        students = [f"{k} - {v['name']}" for k, v in self.students.items()]
        combo = ttk.Combobox(frame, values=students, width=30, font=("Arial", 11))
        combo.grid(row=0, column=1, pady=5, padx=5)
        combo.current(0)
        
        # Marks entries
        marks_frame = tk.Frame(self.root, bg=BG)
        marks_frame.pack(pady=10)
        
        entries = {}
        subjects = ["Math", "English", "Science", "History", "Hindi"]
        
        for i, sub in enumerate(subjects):
            tk.Label(marks_frame, text=f"{sub}:", font=("Arial", 11), bg=BG).grid(row=i, column=0, pady=3, sticky="w")
            e = tk.Entry(marks_frame, font=("Arial", 11), width=10)
            e.grid(row=i, column=1, pady=3, padx=5)
            entries[sub] = e
        
        def save_marks():
            sid = combo.get().split(" - ")[0]
            marks = {}
            
            for sub, entry in entries.items():
                try:
                    val = entry.get().strip()
                    marks[sub] = int(val) if val else 0
                except:
                    messagebox.showerror("Error", "Enter valid numbers!")
                    return
            
            self.students[sid]["marks"] = marks
            self.save_data()
            messagebox.showinfo("Success", "Marks saved!")
            self.show_main_menu()
        
        tk.Button(self.root, text="Save Marks", font=("Arial", 12), bg=GREEN, fg=WHITE,
            command=save_marks).pack(pady=10)
        tk.Button(self.root, text="Back", font=("Arial", 11), command=self.show_main_menu).pack()
    
    # ==================== VIEW RESULTS ====================
    def results_screen(self):
        self.clear()
        
        tk.Label(self.root, text="All Student Results", font=("Arial", 18, "bold"), bg=BG).pack(pady=15)
        
        # Table
        cols = ("ID", "Name", "Class", "Math", "Eng", "Sci", "Hist", "Hindi", "Total", "Avg", "Grade")
        tree = ttk.Treeview(self.root, columns=cols, show="headings", height=15)
        
        widths = [50, 100, 60, 40, 40, 40, 40, 40, 50, 45, 45]
        for col, w in zip(cols, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w)
        
        tree.pack(pady=10)
        
        # Add data
        for sid, data in self.students.items():
            marks = data.get("marks", {})
            
            # Show all students, even without marks
            math = marks.get("Math", "-")
            eng = marks.get("English", "-")
            sci = marks.get("Science", "-")
            hist = marks.get("History", "-")
            hindi = marks.get("Hindi", "-")
            
            if marks:
                total = sum(marks.values())
                avg = total / len(marks)
                g = "A" if avg >= 90 else "B" if avg >= 80 else "C" if avg >= 70 else "D" if avg >= 60 else "F"
            else:
                total = "-"
                avg = "-"
                g = "-"
            
            tree.insert("", tk.END, values=(
                sid, data["name"], data["class"],
                math, eng, sci, hist, hindi,
                total, avg, g
            ))
        
        tk.Button(self.root, text="Back", font=("Arial", 11), command=self.show_main_menu).pack(pady=10)
    
    # ==================== DELETE STUDENT ====================
    def delete_student_screen(self):
        self.clear()
        
        if not self.students:
            tk.Label(self.root, text="No students to delete!", font=("Arial", 14), bg=BG).pack(pady=50)
            tk.Button(self.root, text="Back", command=self.show_main_menu).pack()
            return
        
        tk.Label(self.root, text="Delete Student", font=("Arial", 18, "bold"), bg=BG).pack(pady=15)
        
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(pady=20)
        
        tk.Label(frame, text="Select Student:", font=("Arial", 12), bg=BG).grid(row=0, column=0)
        
        students = [f"{k} - {v['name']}" for k, v in self.students.items()]
        combo = ttk.Combobox(frame, values=students, width=30, font=("Arial", 11))
        combo.grid(row=0, column=1, padx=5)
        combo.current(0)
        
        def delete():
            sid = combo.get().split(" - ")[0]
            name = self.students[sid]["name"]
            
            confirm = messagebox.askyesno("Confirm", f"Delete {name}?")
            if confirm:
                del self.students[sid]
                self.save_data()
                messagebox.showinfo("Success", "Student deleted!")
                self.show_main_menu()
        
        tk.Button(self.root, text="Delete", font=("Arial", 12), bg=RED, fg=WHITE,
            command=delete).pack(pady=10)
        tk.Button(self.root, text="Back", font=("Arial", 11), command=self.show_main_menu).pack()


# Run
if __name__ == "__main__":
    root = tk.Tk()
    StudentSystem(root)
    root.mainloop()