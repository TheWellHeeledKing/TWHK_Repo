import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from send2trash import send2trash
from PIL import Image, ImageTk

# Constants for known file types
KNOWN_FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"],
    "Documents": [".doc", ".docx", ".pdf", ".txt", ".xls", ".xlsx", ".ods"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Others": [".exe", ".dll", ".iso"]
}

def hash_file(file_path):
    """Generate hash of a file's contents for comparison."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def scan_for_duplicates(drive_paths, extensions):
    """Scan for duplicate files based on metadata and hash."""
    file_map = {}

    for drive in drive_paths:
        for root, _, files in os.walk(drive):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    full_path = os.path.join(root, file)
                    try:
                        file_size = os.path.getsize(full_path)
                        creation_date = os.path.getctime(full_path)
                        modification_date = os.path.getmtime(full_path)
                        file_hash = hash_file(full_path)

                        metadata = (file_size, creation_date, modification_date, file_hash)
                        
                        if metadata not in file_map:
                            file_map[metadata] = []
                        file_map[metadata].append(full_path)
                    except (OSError, PermissionError):
                        continue

    duplicates = {k: v for k, v in file_map.items() if len(v) > 1}
    return duplicates

def preview_image(file_path, max_size=(200, 200)):
    """Generate a preview image for display."""
    try:
        img = Image.open(file_path)
        img.thumbnail(max_size)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None

class DuplicateManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Duplicate Manager")
        self.root.geometry("1000x600")

        self.file_types = list(KNOWN_FILE_TYPES.keys())
        self.selected_file_types = []
        self.selected_drives = []
        self.duplicates = {}
        self.preview_label = None

        self.create_widgets()

    def create_widgets(self):
        """Create the main GUI components."""
        # File type selection
        frame_top = tk.Frame(self.root)
        frame_top.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(frame_top, text="Select File Types:").pack(side=tk.LEFT)
        self.file_type_menu = ttk.Combobox(frame_top, values=self.file_types, state="readonly")
        self.file_type_menu.pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_top, text="Add", command=self.add_file_type).pack(side=tk.LEFT, padx=5)

        self.file_type_listbox = tk.Listbox(frame_top, height=5)
        self.file_type_listbox.pack(side=tk.LEFT, padx=10)

        tk.Button(frame_top, text="Remove", command=self.remove_file_type).pack(side=tk.LEFT)

        # Drive selection
        tk.Label(frame_top, text="Drives:").pack(side=tk.LEFT, padx=10)
        self.drive_entry = tk.Entry(frame_top, width=30)
        self.drive_entry.pack(side=tk.LEFT)

        tk.Button(frame_top, text="Add Drive", command=self.add_drive).pack(side=tk.LEFT)

        # Duplicate list
        frame_middle = tk.Frame(self.root)
        frame_middle.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(frame_middle, columns=("Filename", "Drive", "Path", "Creation Date", "Modification Date", "Size"), show="headings")
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="w")
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(frame_middle, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Preview area
        frame_preview = tk.Frame(self.root, height=200)
        frame_preview.pack(fill=tk.X, padx=10, pady=5)

        self.preview_label = tk.Label(frame_preview, text="Preview Area", bg="gray", width=50, height=10)
        self.preview_label.pack()

        # Action buttons
        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(frame_bottom, text="Scan", command=self.scan_duplicates).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_bottom, text="Delete Selected", command=self.delete_selected).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_bottom, text="Exit", command=self.root.destroy).pack(side=tk.RIGHT, padx=5)

    def add_file_type(self):
        """Add a selected file type to the search list."""
        file_type = self.file_type_menu.get()
        if file_type and file_type not in self.selected_file_types:
            self.selected_file_types.append(file_type)
            self.file_type_listbox.insert(tk.END, file_type)

    def remove_file_type(self):
        """Remove a selected file type from the search list."""
        selection = self.file_type_listbox.curselection()
        if selection:
            index = selection[0]
            file_type = self.file_type_listbox.get(index)
            self.selected_file_types.remove(file_type)
            self.file_type_listbox.delete(index)

    def add_drive(self):
        """Add a drive to the search list."""
        drive = self.drive_entry.get()
        if drive and os.path.exists(drive):
            self.selected_drives.append(drive)
            self.drive_entry.delete(0, tk.END)

    def scan_duplicates(self):
        """Scan for duplicates based on selected criteria."""
        extensions = [ext for ft in self.selected_file_types for ext in KNOWN_FILE_TYPES.get(ft, [])]
        if not self.selected_drives or not extensions:
            messagebox.showwarning("Input Missing", "Please select file types and drives.")
            return

        self.duplicates = scan_for_duplicates(self.selected_drives, extensions)

        # Populate the tree with duplicates
        for child in self.tree.get_children():
            self.tree.delete(child)

        for files in self.duplicates.values():
            for file in files:
                file_stat = os.stat(file)
                self.tree.insert("", tk.END, values=(
                    os.path.basename(file),
                    os.path.splitdrive(file)[0],
                    file,
                    file_stat.st_ctime,
                    file_stat.st_mtime,
                    file_stat.st_size
                ))

    def delete_selected(self):
        """Delete selected duplicates."""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "No duplicates selected for deletion.")
            return

        if messagebox.askyesno("Confirm Deletion", "Delete selected duplicates?"):
            for item in selected_items:
                file_path = self.tree.item(item)['values'][2]
                send2trash(file_path)
                self.tree.delete(item)

if __name__ == "__main__":
    root = tk.Tk()
    app = DuplicateManagerApp(root)
    root.mainloop()
