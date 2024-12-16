import os
import polib
import re

# Configuration
SOURCE_DIRS = ["rgb_controller", "common_lib", "rgb_lib", "system_lib"]
LANGUAGES = ["en", "de"]  # Add more language codes as needed
LOCALES_PATH = "locales"
POT_FILE_PATH = os.path.join(LOCALES_PATH, "messages.pot")
TRANSLATE_PATTERN = re.compile(r'translate\([\'"](.+?)[\'"]\)')


# Generate the .pot file
def generate_pot():
    pot = polib.POFile()

    for dir_path in SOURCE_DIRS:
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith(".py"):  # Process Python files only
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        # Process the file line by line to capture line numbers
                        for line_num, line in enumerate(f, start=1):  # `start=1` for 1-based line numbers
                            matches = TRANSLATE_PATTERN.findall(line)
                            for match in matches:
                                entry = pot.find(match)
                                if not entry:
                                    entry = polib.POEntry(
                                        msgid=match,
                                        msgstr="",
                                        occurrences=[(file_path, line_num)]  # Use actual line number
                                    )
                                    pot.append(entry)
                                else:
                                    # Append the new occurrence
                                    if (file_path, line_num) not in entry.occurrences:
                                        entry.occurrences.append((file_path, line_num))  # Avoid duplicates

    os.makedirs(LOCALES_PATH, exist_ok=True)
    pot.save(POT_FILE_PATH)
    print(f"Generated {POT_FILE_PATH}")

# Create or update .po files
def create_or_update_po(language_code):
    po_file_path = os.path.join(LOCALES_PATH, language_code, "messages.po")
    print(f"Creating/Updating: {po_file_path}")
    os.makedirs(os.path.dirname(po_file_path), exist_ok=True)

    # Load .pot file and existing .po file
    pot = polib.pofile(POT_FILE_PATH)
    po = polib.pofile(po_file_path) if os.path.exists(po_file_path) else polib.POFile()

    # Add missing msgid from the .pot file to .po
    for pot_entry in pot:

        po_entry = po.find(pot_entry.msgid)
        if po_entry:  # If msgid exists in the .po file
            po_entry.occurrences = pot_entry.occurrences

            # Format occurrences with newlines
            occurrences_str = "\n".join([f"#: {file}:{line}" for file, line in po_entry.occurrences])
            print(f"Exists: Msgid: {po_entry.msgid} Msgstr: {po_entry.msgstr} Occurrences:\n{occurrences_str}")

        else:
            po.append(pot_entry)

            # Format occurrences with newlines
            occurrences_str = "\n".join([f"#: {file}:{line}" for file, line in pot_entry.occurrences])
            print(f"Exists: Msgid: {pot_entry.msgid} Msgstr: {pot_entry.msgstr} Occurrences:\n{occurrences_str}")

    # Remove obsolete entries (those not in the .pot file)
    print(f"Checking for obsolete msgids: remove if exists in {po_file_path}, no longer in {POT_FILE_PATH}")

    for entry in po:
        if pot.find(entry.msgid):
            print(f"Kept: {entry.msgid} {entry.msgstr}")
        else:
            po.remove(entry)
            print(f"{entry.msgid} {entry.msgstr} deprecated -> delete translation or transfer to replacement msg")
    # Save the updated .po file
    po.save(po_file_path)
    print(f"Updated {po_file_path}")


# Compile .po to .mo files
def compile_po(language_code):
    po_file_path = os.path.join(LOCALES_PATH, language_code, "messages.po")
    mo_file_path = po_file_path.replace(".po", ".mo")
    if not os.path.exists(po_file_path):
        print(f"No .po file for language {language_code}, skipping compilation.")
        return
    po = polib.pofile(po_file_path)
    po.save_as_mofile(mo_file_path)
    print(f"Compiled {mo_file_path}")


# Check .mo file validity
def check_mo(language_code):
    mo_file_path = os.path.join(LOCALES_PATH, language_code, "messages.mo")
    if not os.path.exists(mo_file_path):
        print(f"{mo_file_path} does not exist. Run the compile command first.")
        return

    try:
        with open(mo_file_path, "rb") as f:
            data = f.read()
            if data.startswith(b'\xde\x12\x04\x95'):  # MO file magic number
                print(f"{mo_file_path} is a valid .mo file.")

                mo = polib.mofile(mo_file_path)
                print("MO file loaded successfully. Checking contents...")

                # Print the entries to verify they are loaded
                for entry in mo:
                    print(f"msgid: {entry.msgid:<{50}}, msgstr: {entry.msgstr}")
                
            else:
                print(f"{mo_file_path} is NOT a valid .mo file.")

    except Exception as e:
        print(f"Error reading {mo_file_path}: {e}")


# Perform all actions in sequence
def perform_all_actions():
    print("Starting full locale management process...")
    generate_pot()
    for lang in LANGUAGES:
        create_or_update_po(lang)
    for lang in LANGUAGES:
        compile_po(lang)
    for lang in LANGUAGES:
        check_mo(lang)
    print("Full locale management process completed.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Manage .pot, .po, and .mo files for translations.")
    parser.add_argument("action", nargs="?", choices=["generate", "update", "compile", "check"], help="Action to perform")
    args = parser.parse_args()

    if args.action == "generate":
        generate_pot()
    elif args.action == "update":
        for lang in LANGUAGES:
            create_or_update_po(lang)
    elif args.action == "compile":
        for lang in LANGUAGES:
            compile_po(lang)
    elif args.action == "check":
        for lang in LANGUAGES:
            check_mo(lang)
    else:
        perform_all_actions()
