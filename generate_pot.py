import polib
import os
import re

# Define the directories you want to scan for translatable strings
source_dirs = ['rgb_controller', 'common_lib', 'rgb_lib', 'system_lib']

# Create a new PO file
pot = polib.POFile()

# Define the message extraction pattern (looking for get_translation())
pattern = re.compile(r'get_translation\([\'"](.+?)[\'"]\)')


# Function to extract translatable strings from Python files
def extract_strings_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        return pattern.findall(content)


# Scan source directories
for dir_path in source_dirs:
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.py'):  # Only process Python files
                file_path = os.path.join(root, file)
                translatable_strings = extract_strings_from_file(file_path)
                for string in translatable_strings:
                    # Add the translatable string to the .pot file
                    entry = polib.POEntry(
                        msgid=string,
                        msgstr='',
                        occurrences=[(file_path, 0)]  # Dummy line number
                    )
                    pot.append(entry)

# Save the .pot file in the locales directory
os.makedirs('locales', exist_ok=True)  # Ensure the directory exists
pot.save(os.path.join('locales', 'messages.pot'))

print("Translation template (.pot file) has been generated successfully.")
