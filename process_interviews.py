import os
import docx2txt
import config

INPUT_FOLDER = "data/raw/interviews"

def convert_docx_to_txt():
    # Create the output folder if it doesn't exist
    os.makedirs(config.PROCESSED_DATA, exist_ok=True)

    # Get all DOCX files in the input folder
    docx_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(".docx")]

    if not docx_files:
        print(f"No DOCX files found in {INPUT_FOLDER}")
        return

    for docx_file in docx_files:
        # Construct the full path to the DOCX file
        docx_path = os.path.join(INPUT_FOLDER, docx_file)

        # Generate the output file name with '_interview' suffix
        base_name = os.path.splitext(docx_file)[0]
        txt_file = f"{base_name}_interview.txt"
        txt_path = os.path.join(config.PROCESSED_DATA, txt_file)

        try:
            # Extract text from the DOCX file
            text = docx2txt.process(docx_path)

            # Write to text file
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"Converted {docx_file} to {txt_file}")

        except Exception as e:
            print(f"Error converting {docx_file}: {str(e)}")


if __name__ == "__main__":
    convert_docx_to_txt()
