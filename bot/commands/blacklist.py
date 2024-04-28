import os
import json

# Function to load the blacklist and handle errors
def load_blacklist(blacklist_filename):
    """Loads the blacklist from a JSON file, with error handling."""
    # Get the current script directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full path to the blacklist file
    blacklist_file_path = os.path.join(script_directory, blacklist_filename)
    
    if not os.path.exists(blacklist_file_path):
        print(f"Blacklist file '{blacklist_file_path}' does not exist.")
        return []  # Return an empty list if the file doesn't exist

    if not os.path.isfile(blacklist_file_path):
        print(f"'{blacklist_file_path}' is not a valid file.")
        return []  # Return an empty list if it's not a valid file

    try:
        with open(blacklist_file_path, 'r') as f:
            blacklist = json.load(f)
            if not isinstance(blacklist, list):
                print("Blacklist file content is not a list.")
                return []  # Ensure the content is a list
            print(f"Loaded {len(blacklist)} URLs from the blacklist.")
            return blacklist
    except json.JSONDecodeError:
        print(f"Blacklist file '{blacklist_file_path}' contains invalid JSON.")
        return []  # Return empty if there's a JSON error
    except Exception as e:
        print(f"An error occurred while loading the blacklist: {e}")
        return []  # General exception handling
