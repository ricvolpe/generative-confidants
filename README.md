# Generative confidants

## Data processing steps

1. `process-diaries.py` processes raw diary entries CSV from qualtrics and produces
    * TXT files for each participant's diary entries and chat transcripts
    * CSV file with quantitative measures of diary entries

2. `process-interviews.py` converts DOCX interview transcripts into TXT files
OUTPUT_FOLDER path should be the same for step 1 and 2 to complete step 3

3. `textwash.sh` scans all text files in an input folder (which should be the 
OUTPUT_FOLDER of step 1-2) and generates key-value JSON dictionaries with
explicit identifiers

4. User can go through the output folder of step 3 and review the anonimisation
dictionaries and change them as desires, removing entries or changing the replacement
values

5. `replace_identifiers.py` taxes the input folder with all the TXT files and
the folder with the JSON anonymisation keys and perform the replacements on the
files, creating new copies so that the non-anonymised data is still available

## Conventions

* Replacements use double square brackets. For example:
    - [[NAME]]
    - [[LOCATION]]
    - or [[REDACTED]]

* In the anonymised chat and interview transcripts, empty lines (i.e. `/n/n`) 
indicate a change in speaker from human to AI or vice versa