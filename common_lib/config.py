import logging

# Constants to control runs if debugging or not
# Set DEBUG_LEVEL to logging.INFO for live runs or logging.DEBUG for debugging
# If running from IDE / cmd no wait necessary, otherwise set as necessary

DEBUG_LEVEL = logging.INFO
CLOSE_SCRIPT_WAIT_SECS = 5

# Constants for logging
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Any other constants can be added here
MAIN = "__main__"

# Initialize translation constants. Change language here
LANGUAGE = "de"
# Define path to the .mo file for the specified language
MO_PATH_AND_FILENAME = f"locales/{LANGUAGE}/LC_MESSAGES/messages.mo"
