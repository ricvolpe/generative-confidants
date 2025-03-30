import os
import json
import shutil
import config

KEYS_FOLDER = 'anon_keys'

def process_files():
    """
    Process each TXT file in the input folder by replacing keys with values
    from a matching JSON file, and save the result to the output folder.
    """
    # Create the output folder if it doesn't exist
    os.makedirs(config.ANON_DATA, exist_ok=True)
    
    # Get all TXT files in the input folder
    txt_files = [f for f in os.listdir(config.PROCESSED_DATA) if f.endswith('.txt')]
    
    for txt_file in txt_files:
        # Get the base name without extension
        base_name = os.path.splitext(txt_file)[0]
        
        # Construct the JSON file path
        json_file = os.path.join(config.PROCESSED_DATA, f"{KEYS_FOLDER}/{base_name}.json")
        print(json_file)
        # Check if the corresponding JSON file exists
        if not os.path.exists(json_file):
            # If not, just copy the TXT file to the output folder
            shutil.copy2(
                os.path.join(config.PROCESSED_DATA, txt_file),
                os.path.join(config.ANON_DATA, txt_file)
            )
            print(f"No JSON file found for {txt_file}. Copied without changes.")
            continue
        
        # Read the TXT file content
        with open(os.path.join(config.PROCESSED_DATA, txt_file), 'r', encoding='utf-8') as f:
            txt_content = f.read()
        
        # Read the JSON file
        with open(json_file, 'r', encoding='utf-8') as f:
            try:
                replacements = json.load(f)
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON in {json_file}. Skipping replacements.")
                # Still copy the original file to output
                shutil.copy2(
                    os.path.join(config.PROCESSED_DATA, txt_file),
                    os.path.join(config.ANON_DATA, txt_file)
                )
                continue
        
        # Replace each key with its value in the TXT content
        for key, value in replacements.items():
            txt_content = txt_content.replace(key, "[[" + str(value) + "]]")
        
        # Write the modified content to the output folder
        with open(os.path.join(config.ANON_DATA, txt_file), 'w', encoding='utf-8') as f:
            f.write(txt_content)
        
        print(f"Processed {txt_file} with replacements from {base_name}.json")

if __name__ == "__main__":    
    process_files()