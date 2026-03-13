import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
from tkinter import font
import os

class Noty:
    def __init__(self, root):
        self.root = root
        self.root.title("Noty Pro")
        self.root.geometry("900x600")

        # BUG 2 FIX: per-tab file tracking instead of one shared self.current_file
        self.tab_files = {}   # { tab_frame_name : file_path }
        self.recent_files = []

        self.setup_ui()
        self.setup_menu()
        self.auto_save()

    # ---------------- UI SETUP ---------------- #
    def setup_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar Explorer
        self.tree = ttk.Treeview(self.main_frame)
        self.tree.pack(side="left", fill="y")
        self.tree.bind("<Double-1>", self.open_from_tree)

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True)

        self.create_new_tab()

        # Status Bar
        self.status = tk.Label(self.root, text="Line: 1 | Column: 1", anchor="e")
        self.status.pack(fill="x", side="bottom")

    # ---------------- TAB MANAGEMENT ---------------- #
    def create_new_tab(self, content=""):
        frame = tk.Frame(self.notebook)
        text = tk.Text(frame, wrap="word", undo=True)
        text.pack(fill="both", expand=True)
        text.insert("1.0", content)

        # BUG 1 FIX: use add=True so both binds fire, not just the last one
        text.bind("<KeyRelease>", self.update_status,      add=True)

        self.notebook.add(frame, text="Untitled")
        self.notebook.select(frame)

        # BUG 2 FIX: register this tab with no file path yet
        self.tab_files[str(frame)] = None

    # BUG 6 FIX: safe getter — returns None if no tab is open
    def get_text_widget(self):
        try:
            selected = self.notebook.select()
            if not selected:
                return None
            return self.notebook.nametowidget(selected).winfo_children()[0]
        except Exception:
            return None

    # BUG 2 FIX: helper to get/set file for currently active tab
    def get_current_tab_frame(self):
        try:
            return self.notebook.select()
        except Exception:
            return None

    # ---------------- FILE FUNCTIONS ---------------- #
    def new_file(self):
        self.create_new_tab()

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.create_new_tab(content)
            tab = self.get_current_tab_frame()
            self.notebook.tab(tab, text=os.path.basename(file_path))
            # BUG 2 FIX: store file path per tab, not globally
            self.tab_files[str(tab)] = file_path
            self.add_recent(file_path)

    def save_file(self):
        text = self.get_text_widget()
        if text is None:
            return

        tab = self.get_current_tab_frame()
        # BUG 2 FIX: look up file path from per-tab dict
        current_file = self.tab_files.get(str(tab))

        if not current_file:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt")
            if not file_path:
                return
            self.tab_files[str(tab)] = file_path
            self.notebook.tab(tab, text=os.path.basename(file_path))
        else:
            file_path = current_file

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text.get("1.0", tk.END))

        messagebox.showinfo("Saved", "File saved successfully!")

    # ---------------- STATUS ---------------- #
    def update_status(self, event=None):
        text = self.get_text_widget()
        if text is None:
            return
        row, col = text.index(tk.INSERT).split(".")
        self.status.config(text=f"Line: {row} | Column: {int(col)+1}")

    # ---------------- WORD COUNT ---------------- #
    def word_count(self):
        text = self.get_text_widget()
        if text is None:
            return
        words = len(text.get("1.0", tk.END).split())
        messagebox.showinfo("Word Count", f"Total words: {words}")

    # ---------------- SEARCH ---------------- #
    def find_text(self):
        text = self.get_text_widget()
        if text is None:
            return
        search = simpledialog.askstring("Find", "Enter text:")
        if search:
            text.tag_remove("highlight", "1.0", tk.END)
            start = "1.0"
            found = False
            while True:
                start = text.search(search, start, stopindex=tk.END)
                if not start:
                    break
                found = True
                end = f"{start}+{len(search)}c"
                text.tag_add("highlight", start, end)
                start = end
            text.tag_config("highlight", background="yellow")

            if not found:
                messagebox.showinfo("Find", f"{search!r} not found.")

            # Auto-clear highlights when user starts typing again
            text.bind("<KeyPress>", self.clear_highlights, add=True)

    def clear_highlights(self, event=None):
        text = self.get_text_widget()
        if text is None:
            return
        text.tag_remove("highlight", "1.0", tk.END)
        # Unbind so it does not fire on every keypress after clearing
        text.unbind("<KeyPress>")

    # ---------------- AUTO SAVE ---------------- #
    def auto_save(self):
        # BUG 5 FIX: wrap in try/except so a write failure doesn't crash the app
        try:
            text = self.get_text_widget()
            if text is not None:
                autosave_path = os.path.join(os.path.expanduser("~"), "autosave.txt")
                with open(autosave_path, "w", encoding="utf-8") as f:
                    f.write(text.get("1.0", tk.END))
        except Exception:
            pass  # silently skip if autosave fails
        self.root.after(5000, self.auto_save)

    # ---------------- THEME ---------------- #
    def set_dark(self):
        text = self.get_text_widget()
        if text:
            text.config(bg="#1e1e1e", fg="white", insertbackground="white")

    def set_light(self):
        text = self.get_text_widget()
        if text:
            text.config(bg="white", fg="black", insertbackground="black")

    # ---------------- FONT ---------------- #
    def change_font(self):
        text = self.get_text_widget()
        if text:
            text.config(font=("Courier", 14))


    # ---------------- RECENT FILES ---------------- #
    def add_recent(self, file_path):
        if file_path not in self.recent_files:
            self.recent_files.append(file_path)
        if len(self.recent_files) > 5:
            self.recent_files.pop(0)

    # ---------------- FILE EXPLORER ---------------- #
    def load_directory(self):
        folder = filedialog.askdirectory()
        if folder:
            self.tree.delete(*self.tree.get_children())
            for file in os.listdir(folder):
                full_path = os.path.join(folder, file)
                self.tree.insert("", "end", text=file, values=[full_path])

    def open_from_tree(self, event):
        item = self.tree.selection()
        if item:
            # BUG 4 FIX: use values[0] (full path) not text (filename only)
            values = self.tree.item(item)["values"]
            if not values:
                return
            file_path = values[0]
            if os.path.isfile(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    self.create_new_tab(f.read())
                tab = self.get_current_tab_frame()
                self.notebook.tab(tab, text=os.path.basename(file_path))
                self.tab_files[str(tab)] = file_path

    # ---------------- MENU ---------------- #
    def setup_menu(self):
        menu = tk.Menu(self.root)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="New",         command=self.new_file)
        file_menu.add_command(label="Open",        command=self.open_file)
        file_menu.add_command(label="Save",        command=self.save_file)
        file_menu.add_command(label="Open Folder", command=self.load_directory)
        file_menu.add_separator()
        file_menu.add_command(label="Exit",        command=self.root.quit)

        tools_menu = tk.Menu(menu, tearoff=0)
        tools_menu.add_command(label="Word Count",      command=self.word_count)
        tools_menu.add_command(label="Find",            command=self.find_text)
        tools_menu.add_command(label="Clear Highlights", command=self.clear_highlights)
        tools_menu.add_command(label="Change Font",     command=self.change_font)

        theme_menu = tk.Menu(menu, tearoff=0)
        theme_menu.add_command(label="Dark Mode",  command=self.set_dark)
        theme_menu.add_command(label="Light Mode", command=self.set_light)

        menu.add_cascade(label="File",  menu=file_menu)
        menu.add_cascade(label="Tools", menu=tools_menu)
        menu.add_cascade(label="Theme", menu=theme_menu)

        self.root.config(menu=menu)


# ---------------- RUN APP ---------------- #
root = tk.Tk()
app = Noty(root)
root.mainloop()