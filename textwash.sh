# Step 0 > Activate conda environment
source ~/Programs/miniconda3/bin/activate textwash 

# Step 1 > Change directory
cd ~/Programs/Python/textwash

# Step 2 > Run the Python script with the variables
python3 anon.py \
    --language en \
    --input_dir "/Users/Ric/Programs/trust-me/gen-confidants/data/processed/pilot" \
    --output_dir "/Users/Ric/Programs/trust-me/gen-confidants/data/processed/pilot/anon_keys" \
    --cpu \
    --entities ADDRESS,AGE,EMAIL_ADDRESS,LOCATION,OCCUPATION,ORGANIZATION,OTHER,PERSON_FIRSTNAME,PERSON_LASTNAME,PHONE_NUMBER

# Time measurments
3 diary entries with transcripts: 55s