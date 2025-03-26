import os
import pandas as pd
import re

FILE_PATH = 'data/raw/diaries_pilot.csv'
COLUMS = {
    'pseudonym': 'QID4_TEXT',
    'transcript': 'QID6_TEXT',
    'ai': 'QID5',
    'diary': ['QID5', 'QID8_TEXT', 'QID9_TEXT', 'QID10_TEXT', 'QID11_TEXT', 
              'QID12_TEXT', 'QID13_TEXT', 'QID14_TEXT', 'QID15', 'QID16',
              'QID17', 'QID18_TEXT'],
}
OUTPUT_FOLDER = 'data/1_processed'

def process_csv(file_path):
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    
    df = pd.read_csv(file_path)
    df['entry_number'] = df.groupby(COLUMS['pseudonym']).cumcount() + 1
    question_texts = df.iloc[0]
    for index, row in df.iterrows():
        if index == 0: continue # skip 1st row with question text
        pseudonym = row[COLUMS['pseudonym']].lower().replace(' ', '-')
        create_transcript(row, pseudonym)
        create_diary(row, pseudonym, question_texts)

    reformatted_df = pd.DataFrame({
        'pseudonym': df[COLUMS['pseudonym']], 'entry_number': df['entry_number'],
        'start': df['startDate'], 'end': df['endDate'], 'duration': df['duration'],
        'platform': df['QID5'],
        'satisfaction': df['QID15'], 'trust': df['QID16'],
    })
    reformatted_df = reformatted_df.iloc[1:].reset_index(drop=True)
    reformatted_df.to_csv('data/diaries_pilot_quant.csv', index=False)

def create_transcript(row, pseudonym):
    chat_transcript = row[COLUMS['transcript']]
    if not pd.isna(chat_transcript) and chat_transcript != '':
        chat_filename = f"{pseudonym}_{row['entry_number']}_transcript.txt"
        chat_path = os.path.join(OUTPUT_FOLDER, chat_filename)
        cleaned_transcript = clean_transcript(chat_transcript)
        with open(chat_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_transcript)

def clean_transcript(text):
    if text is None or not isinstance(text, str):
        return None
    return re.sub(r'\n{3,}', '\n\n', text).strip()

def create_diary(row, pseudonym, question_texts):
    diary_filename = f"{pseudonym}_{row['entry_number']}_diary.txt"
    diary_path = os.path.join(OUTPUT_FOLDER, diary_filename)
    with open(diary_path, 'w', encoding='utf-8') as f:
        for question in COLUMS['diary']:
            f.write(question_texts[question].split('.')[0].split('?')[0])
            f.write("\n")
            if not pd.isna(row[question]):
                f.write(row[question])
                f.write("\n\n")

if __name__ == "__main__":
    process_csv(FILE_PATH)
    print("Processing complete.")