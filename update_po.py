import os
import polib

# Paths to the .pot and .po files
POT_FILE_PATH = 'locales/messages.pot'
PO_FILE_PATH = 'locales/en/LC_MESSAGES/messages.po'

# Ensure the directory for the .po file exists
os.makedirs(os.path.dirname(PO_FILE_PATH), exist_ok=True)

# Load the .pot file
pot = polib.pofile(POT_FILE_PATH)

# Load or create the .po file
if os.path.exists(PO_FILE_PATH):
    po = polib.pofile(PO_FILE_PATH)
else:
    po = polib.POFile()

# Update the .po file with entries from the .pot file
for entry in pot:
    existing_entry = po.find(entry.msgid)
    if existing_entry:
        # If entry exists, keep its translation
        existing_entry.occurrences = entry.occurrences
    else:
        # If entry doesn't exist, add it as untranslated
        po.append(entry)

# Save the updated .po file
po.save(PO_FILE_PATH)

print(f"Translation file updated: {PO_FILE_PATH}")
