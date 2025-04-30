import os
import pandas as pd
import re
import config

def process_csv():
    if not os.path.exists(config.PROCESSED_DATA):
        os.makedirs(config.PROCESSED_DATA)
    
    df = pd.read_csv(config.QTRICS_CSV)
    df['entry_number'] = df.groupby(config.QTRICS_COLS['pseudonym']).cumcount() + 1
    question_texts = df.iloc[0]
    for index, row in df.iterrows():
        if index == 0: continue # skip 1st row with question text
        pseudonym = row[config.QTRICS_COLS['pseudonym']].lower().replace(' ', '-')
        if pseudonym in config.PSEUDOS_INCLUDE:
            create_transcript(row, pseudonym)
            create_diary(row, pseudonym, question_texts)

def create_transcript(row, pseudonym):
    chat_transcript = row[config.QTRICS_COLS['transcript']]
    if not pd.isna(chat_transcript) and chat_transcript != '':
        chat_filename = f"{pseudonym}_{row['entry_number']}_transcript.txt"
        chat_path = os.path.join(config.PROCESSED_DATA, chat_filename)
        cleaned_transcript = clean_transcript(chat_transcript)
        with open(chat_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_transcript)

def clean_transcript(text):
    if text is None or not isinstance(text, str):
        return None
    return re.sub(r'\n{3,}', '\n\n', text).strip()

def create_diary(row, pseudonym, question_texts):
    diary_filename = f"{pseudonym}_{row['entry_number']}_diary.txt"
    diary_path = os.path.join(config.PROCESSED_DATA, diary_filename)
    with open(diary_path, 'w', encoding='utf-8') as f:
        for question in config.QTRICS_COLS['diary']:
            f.write(question_texts[question].split('.')[0].split('?')[0])
            f.write("?\n")
            if not pd.isna(row[question]):
                f.write(row[question])
                f.write("\n\n")

if __name__ == "__main__":
    process_csv()
    print("Processing complete.")