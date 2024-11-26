import polib
import os

# Path to the 'locales' directory
locales_dir = os.path.join(os.path.dirname(__file__), "locales")
mo_file_path = os.path.join(locales_dir, "en", "LC_MESSAGES", "messages.mo")

# Try to read the MO file
try:
    po = polib.mofile(mo_file_path)
    print("MO file loaded successfully. Checking contents...")

    # Print some of the entries to verify they are loaded
    for entry in po:
        print(f"msgid: {entry.msgid}, msgstr: {entry.msgstr}")

except Exception as e:
    print(f"Error loading MO file: {e}")
