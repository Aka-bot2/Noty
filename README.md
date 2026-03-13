# 📝 Noty Pro

A lightweight desktop notepad app built with Python and Tkinter. Supports tabbed editing, file exploration, find & highlight, themes, and auto-save — no external dependencies required.

---

## Features

- **Tabbed editing** — open multiple files at once, each in its own tab
- **File explorer sidebar** — browse and open files from a folder directly in the app
- **Find & highlight** — search for text with yellow highlights; clears automatically when you start typing
- **Auto-save** — silently saves your current work every 5 seconds to `~/autosave.txt`
- **Word count** — quick word count for the active tab
- **Dark / Light theme** — toggle between dark (`#1e1e1e`) and light mode
- **Font change** — switch to Courier 14pt
- **Recent files** — tracks the last 5 opened files
- **Status bar** — shows current line and column number

---

## Requirements

- Python 3.x
- Tkinter (comes bundled with most Python installations)

No `pip install` needed.

---

## Running the App

```bash
python noty1.py
```

---

## Usage

| Menu | Option | Description |
|------|--------|-------------|
| File | New | Opens a new blank tab |
| File | Open | Opens a file in a new tab |
| File | Save | Saves the current tab (prompts for path if unsaved) |
| File | Open Folder | Loads a folder into the sidebar explorer |
| File | Exit | Closes the app |
| Tools | Word Count | Shows total word count for the current tab |
| Tools | Find | Highlights all matches in the current tab |
| Tools | Clear Highlights | Removes all search highlights |
| Tools | Change Font | Switches to Courier 14pt |
| Theme | Dark Mode | Dark background with white text |
| Theme | Light Mode | White background with black text |

---

## Project Structure

```
noty1.py   # Single-file app — all logic lives here
```

---

## Known Limitations

- Font change is fixed to Courier 14pt (no font picker dialog yet)
- Recent files list is in-memory only — resets when the app closes
- Auto-save only saves the currently active tab

---

## Built With

- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) — Python's standard GUI library
