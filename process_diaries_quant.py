import os
import pandas as pd
import config

def process_csv():
    if not os.path.exists(config.PROCESSED_DATA):
        os.makedirs(config.PROCESSED_DATA)
    
    df = pd.read_csv(config.QTRICS_CSV)
    df['entry_number'] = df.groupby(config.QTRICS_COLS['pseudonym']).cumcount() + 1
    platform_values = df['Q4'].copy()
    other_mask = df['Q4'] == "Other"
    platform_values.loc[other_mask] = df.loc[other_mask, 'Q4_7_TEXT']

    reformatted_df = pd.DataFrame({
        'pseudonym': df[config.QTRICS_COLS['pseudonym']], 
        'entry_number': df['entry_number'],
        'submittedAt': df['EndDate'],
        'platform': platform_values,
        'satisfaction': df['Q13'], 
        'trust': df['Q14'],
    })
    reformatted_df = reformatted_df.iloc[2:].reset_index(drop=True)
    reformatted_df.to_csv(config.QUANT_FILE, index=False)

if __name__ == "__main__":
    process_csv()
    print("Processing complete.")