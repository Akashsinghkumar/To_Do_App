import customtkinter as ctk
import sqlite3
import time
import webbrowser

DB_NAME = "todo.db"
MAX_TASKS = 999

# --------------------
# DATABASE FUNCTIONS
# --------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_task_to_db(text):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    created_time = time.strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO tasks (text, completed, created_at) VALUES (?, 0, ?)",
              (text, created_time))
    conn.commit()
    conn.close()

def delete_task_from_db(task_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def toggle_task(task_id, completed):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, text, completed, created_at FROM tasks ORDER BY id ASC")
    rows = c.fetchall()
    conn.close()
    return rows


# --------------------
# MAIN APP CLASS
# --------------------
class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("To-Do List Premium (Canva UI)")
        self.geometry("600x750")

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # --------- HEADER ---------
        header = ctk.CTkFrame(self, corner_radius=20)
        header.pack(fill="x", padx=20, pady=20)

        self.title_entry = ctk.CTkEntry(header, placeholder_text="My To-Do List",
                                        font=("Poppins", 24, "bold"), width=400)
        self.title_entry.pack(pady=(20, 5))

        self.subtitle_entry = ctk.CTkEntry(header,
                                           placeholder_text="Get things done ✨",
                                           font=("Poppins", 14), width=400)
        self.subtitle_entry.pack(pady=(0, 20))

        # --------- ADD TASK AREA ---------
        input_frame = ctk.CTkFrame(self, corner_radius=20)
        input_frame.pack(fill="x", padx=20)

        self.task_entry = ctk.CTkEntry(input_frame, placeholder_text="Add new task...",
                                       font=("Poppins", 14), width=400)
        self.task_entry.pack(side="left", padx=10, pady=15)

        add_btn = ctk.CTkButton(input_frame, text="Add Task",
                                command=self.add_task, font=("Poppins", 14))
        add_btn.pack(side="left", padx=10)

        # --------- STATS ---------
        self.stats_label = ctk.CTkLabel(self, text="Total: 0 | Active: 0 | Completed: 0",
                                        font=("Poppins", 12))
        self.stats_label.pack(pady=10)

        # --------- TASK LIST ---------
        self.task_frame = ctk.CTkScrollableFrame(self, corner_radius=20, width=550, height=430)
        self.task_frame.pack(padx=20, pady=10)

        # --------- FOOTER ---------
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(pady=10)

        ctk.CTkLabel(footer, text="Developed By AKASH KUMAR",
                     font=("Poppins", 12, "bold")).pack()

        link_row = ctk.CTkFrame(footer, fg_color="transparent")
        link_row.pack()

        ctk.CTkButton(link_row, text="GitHub", width=80, fg_color="white",
                      hover_color="#DDDDDD", text_color="blue",
                      command=lambda: webbrowser.open("https://github.com/Akash")
                      ).pack(side="left", padx=10)

        ctk.CTkButton(link_row, text="LinkedIn", width=80, fg_color="white",
                      hover_color="#DDDDDD", text_color="blue",
                      command=lambda: webbrowser.open("https://linkedin.com/in/Akash")
                      ).pack(side="left")

        # Load existing tasks
        self.load_tasks()

    # --------------------
    # FUNCTIONALITY
    # --------------------
    def add_task(self):
        text = self.task_entry.get().strip()
        if not text:
            return

        add_task_to_db(text)
        self.task_entry.delete(0, "end")
        self.load_tasks()

    def load_tasks(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        tasks = get_tasks()

        total = len(tasks)
        completed = sum(1 for t in tasks if t[2] == 1)
        active = total - completed

        self.stats_label.configure(
            text=f"Total: {total} | Active: {active} | Completed: {completed}"
        )

        for task_id, text, comp, created in tasks:
            row = ctk.CTkFrame(self.task_frame, corner_radius=15)
            row.pack(fill="x", pady=5, padx=10)

            check = ctk.CTkCheckBox(row, text=text, width=400,
                                    onvalue=1, offvalue=0,
                                    command=lambda id=task_id, chk=comp:
                                    self.toggle_task(id, chk))
            check.pack(side="left", padx=10, pady=10)

            if comp:
                check.select()

            del_btn = ctk.CTkButton(row, text="Delete", width=60,
                                    fg_color="#DD4444", hover_color="#BB3333",
                                    command=lambda id=task_id:
                                    self.delete_task(id))
            del_btn.pack(side="right", padx=10)

    def toggle_task(self, task_id, completed):
        new_state = 0 if completed == 1 else 1
        toggle_task(task_id, new_state)
        self.load_tasks()

    def delete_task(self, task_id):
        delete_task_from_db(task_id)
        self.load_tasks()


# --------------------
# RUN APP
# --------------------
init_db()
TodoApp().mainloop()
