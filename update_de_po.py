import polib
import os

# Define file paths
POT_FILE_PATH = 'locales/messages.pot'
DE_PO_FILE_PATH = 'locales/de/LC_MESSAGES/messages.po'

# Load the .pot file
pot = polib.pofile(POT_FILE_PATH)

# Load the German .po file
de_po = polib.pofile(DE_PO_FILE_PATH)

# Add missing msgids from the .pot file to the German .po file
for entry in pot:
    if not de_po.find(entry.msgid):  # If msgid does not exist in the German .po file
        de_po.append(polib.POEntry(
            msgid=entry.msgid,
            msgstr=""  # Leave msgstr empty for now or provide a default translation
        ))
        print(f"Added msgid: {entry.msgid}")  # Log added msgid
    else:
        print(f"msgid already exists: {entry.msgid}")  # Log existing msgid

# Save the updated German .po file
de_po.save(DE_PO_FILE_PATH)

print(f"Updated German .po file saved at: {DE_PO_FILE_PATH}")
