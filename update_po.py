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
        # If entry exists, update occurrences and set msgstr to msgid if it's empty
        existing_entry.occurrences = entry.occurrences
        if not existing_entry.msgstr:
            existing_entry.msgstr = existing_entry.msgid
    else:
        # If entry doesn't exist, add it with msgstr = msgid
        new_entry = polib.POEntry(
            msgid=entry.msgid,
            msgstr=entry.msgid,
            occurrences=entry.occurrences
        )
        po.append(new_entry)

# Save the updated .po file
po.save(PO_FILE_PATH)

print(f"Translation file updated: {PO_FILE_PATH}")
