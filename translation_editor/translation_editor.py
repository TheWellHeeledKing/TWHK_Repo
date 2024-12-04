import os
import json
import polib
import tkinter as tk
from tkinter import ttk, messagebox
import sys
from collections import defaultdict
import numpy as np

# Helper function to load .po files
def load_po_files(language_code):
    locales_dir = os.path.join(os.getcwd(), 'locales')
    po_files = {}
    for lang_folder in os.listdir(locales_dir):
        po_file_path = os.path.join(locales_dir, lang_folder, 'messages.po')
        if os.path.exists(po_file_path):
            po_files[lang_folder] = polib.pofile(po_file_path)
    return po_files

# Helper function to load or create the lock files
def load_lock_files():
    lock_file = os.path.join(os.getcwd(),'locales', 'lang_edit_lock.json')
    if not os.path.exists(lock_file):
        with open(lock_file, 'w') as f:
            json.dump([], f)
    with open(lock_file, 'r') as f:
        lock_data = json.load(f)
    return lock_data

# Function to save lock data
def save_lock_data(lock_data):
    lock_file = os.path.join(os.getcwd(),'locales', 'lang_edit_lock.json')
    with open(lock_file, 'w') as f:
        json.dump(lock_data, f)

# Main GUI function
class TranslationEditorApp:
    def __init__(self, root, language_code="en"):
        self.root = root
        self.language_code = language_code
        self.po_files = load_po_files(language_code)
        self.lock_data = load_lock_files()
        self.entries = []
        self.unsaved_changes = False  # Track unsaved changes

        self.root.title(f"Translation Editor - {language_code}")
        self.create_widgets()

    def update_table_with_filtered_entries(self, filtered_entries):
        # Update the table to show only the filtered entries
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        for entry in filtered_entries:
            self.treeview.insert("", "end", values=entry)

    
    def create_widgets(self):
        # Create a filter frame for msgid type selection (first row)
        msgtype_filter_frame = tk.Frame(self.root)
        msgtype_filter_frame.pack(fill=tk.X)

        # MsgType filter with drop-down
        msgtype_filter_label = tk.Label(msgtype_filter_frame, text="Filter by MsgType:")
        msgtype_filter_label.pack(side=tk.LEFT, padx=5)

        self.msgtype_filter_var = tk.StringVar()
        self.msgtype_filter_var.trace("w", self.apply_filters)

        # Initially populate msgid_filter_menu from empty list (will be updated in load_entries)
        self.msgtype_filter_menu = ttk.Combobox(msgtype_filter_frame, textvariable=self.msgtype_filter_var, values=[], state="readonly")
        self.msgtype_filter_menu.pack(side=tk.LEFT, padx=5, fill=tk.X)

        # Create a filter frame for the text filters (second row)
        text_filters_frame = tk.Frame(self.root)
        text_filters_frame.pack(fill=tk.X)

        # Create the Treeview (table) widget before creating column filters
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Configure grid layout for dynamic resizing
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Set up the table columns
        self.treeview = ttk.Treeview(table_frame, columns=["msgid"] + list(self.po_files.keys()), show="headings")

        # Msgid column header
        self.treeview.heading("msgid", text="msgid") #  Is this necessary? Column header set in prev line of code?
        for lang in self.po_files.keys():
            self.treeview.heading(lang, text=lang)

        # Add vertical and horizontal scrollbars
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.treeview.yview)
        y_scroll.grid(row=0, column=1, sticky="ns")

        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.treeview.xview)
        x_scroll.grid(row=1, column=0, sticky="ew")

        self.treeview.config(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Place the Treeview widget using grid
        self.treeview.grid(row=0, column=0, sticky="nsew")

        # Create a list of tk.StringVar() which will hold the filter strings for each column
        self.text_filter_vars: list[tk.StringVar] = []

        # Now create a list of entry widgets for the text filter for each col
        self.text_filter_entry_fields: list[tk.Entry] = []

        for i, col in enumerate(self.treeview['columns']):

            entry_field = tk.Entry(text_filters_frame)
            self.text_filter_entry_fields.append(entry_field)
            self.text_filter_entry_fields[i].pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

            text_filter_var = tk.StringVar()
            self.text_filter_vars.append(text_filter_var)
            self.text_filter_vars[i].trace("w", self.apply_filters)
            
            # Attach the StringVar to the Entry widget
            self.text_filter_entry_fields[i].config(textvariable=self.text_filter_vars[i])

        # Create Save and Cancel buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, pady=10)

        save_button = tk.Button(button_frame, text="Save", command=self.save_translations)
        save_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=self.cancel_changes)
        cancel_button.pack(side=tk.LEFT, padx=5)

        # Call load_entries to populate entries and filter menu
        self.load_entries()

    def apply_filters(self, *args):

        # Although the args are not needed, the trace method on a StringVar 
        # passes four arguments the callback function, i.e. to apply_filters
        # Omitting the *args leads to a TypeError exception at runtime 

        # Get the msgtype filter for applying to the msgid column (column 0)
        msgtype_filter: str = self.msgtype_filter_var.get().lower()

        column_filters: str = []
        MSGID_COL: int = 0
        filtered_entries = []

        # Get all the column filters
        for text_filter_var in self.text_filter_vars:
            column_filters.append(text_filter_var.get().lower())  # Get the current text from the StringVar

        # Loop through each entry (row) in self.entries (The translations table)
        for entry in self.entries:

            msgtype_match: bool = False
            column_matches = []

            msgid: str = entry[MSGID_COL].lower()

            # Check if the entry's msgtype_filter is not empty, is "All" matches the start of the msgid
            if msgtype_filter == "all":
                msgtype_match = True
            elif (msgtype_filter and msgid.startswith(msgtype_filter)):
                msgtype_match = True

            # If any of the column filters match, then the row is matched
            for column_filter, column_text in zip(column_filters, entry):
                if column_filter == "" or column_filter in str(column_text).lower():
                    column_matches.append(True)
                else:
                    column_matches.append(False)

            if msgtype_match and all(column_matches):
                filtered_entries.append(entry)

        # Update the table with filtered entries
        self.update_table_with_filtered_entries(filtered_entries)


    def update_table_with_filtered_entries(self, filtered_entries):
        # Update the table to show only the filtered entries
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        for entry in filtered_entries:
            self.treeview.insert("", "end", values=entry)

    def update_msgid_filter(self):
        # Extract prefixes from msgid column
        valid_prefixes = {"DEBUG", "ERROR", "INFO", "WORD", "TEXT"}
        
        # Create a set of prefixes from the msgid column of entries
        prefixes = {entry[0].split('_')[0] for entry in self.entries}
        
        # Intersect with the valid prefixes to ensure only valid prefixes are included
        valid_prefixes_in_entries = valid_prefixes.intersection(prefixes)
        
        # Populate the drop-down menu with valid prefixes and add "All" as the first option
        self.msgtype_filter_menu['values'] = ["All"] + sorted(valid_prefixes_in_entries)
        
        # Optionally, set the default selection (e.g., "All")
        self.msgtype_filter_menu.set("All")
        
    def load_entries(self):
        # Get the entries from the po files
        self.entries = []
        for entry in self.po_files[self.language_code]:
            msgid = entry.msgid
            msgstrs = {lang: self.get_msgstr(lang, msgid) for lang in self.po_files.keys()}
            self.entries.append([msgid] + list(msgstrs.values()))
        
        # Sort entries by msgid in ascending order
        self.entries.sort(key=lambda x: x[0])

        # Update the table with the sorted entries
        self.update_table()

        # Populate the msgid filter drop-down menu after loading entries
        self.update_msgid_filter()  # Add this to update the filter


    def get_msgstr(self, lang, msgid):
        po_file = self.po_files.get(lang)
        if po_file:
            entry = po_file.find(msgid)
            if entry:
                return entry.msgstr
        return ""

    def update_table(self):
        # Update table with entries
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        
        for entry in self.entries:
            self.treeview.insert("", "end", values=entry)

    def apply_filter(self, *args):
        # Apply the filter to the table
        filter_text = self.filter_var.get().lower()
        filtered_entries = [
            entry for entry in self.entries if filter_text in entry[0].lower() or any(filter_text in str(msg).lower() for msg in entry[1:])
        ]
        self.entries = filtered_entries
        self.update_table()

    def save_translations(self):
        # Save the updated translations back to .po files
        for lang, po_file in self.po_files.items():
            for entry in self.entries:
                msgid = entry[0]
                msgstr = entry[1 + list(self.po_files.keys()).index(lang)]
                po_entry = po_file.find(msgid)
                if po_entry:
                    po_entry.msgstr = msgstr
            po_file.save(os.path.join(os.getcwd(), 'locales', lang, 'messages.po'))
        
        # Save lock data if any changes occurred
        if self.unsaved_changes:
            self.save_lock_data(self.lock_data)
            self.unsaved_changes = False
        
        messagebox.showinfo("Saved", "Translations saved successfully!")

    def cancel_changes(self):
        # Confirm before cancelling unsaved changes
        if self.unsaved_changes:
            confirm = messagebox.askyesno("Cancel", "You have unsaved changes. Are you sure you want to cancel?")
            if confirm:
                self.load_entries()  # Reload entries to discard changes
        else:
            self.root.quit()

    def lock_language_column(self, lang):
        # Lock a language column if it is locked
        if lang in self.lock_data:
            return True  # Return True if locked
        return False

    def edit_entry(self, event):
        # Enable editing only if the column is not locked
        column = self.treeview.identify_column(event.x)
        lang = column[1:]  # Get the language from the column
        if self.lock_language_column(lang):
            messagebox.showwarning("Locked", f"Editing for {lang} is locked by another user.")
            return False  # Prevent editing if locked
        return True
        

# Start the application
if __name__ == "__main__":

    try:

        lang_code = sys.argv[1] if len(sys.argv) > 1 else "en"
        root = tk.Tk()
        app = TranslationEditorApp(root, language_code=lang_code)
        root.mainloop()

    except Exception as e:
        print(f"{e}")
