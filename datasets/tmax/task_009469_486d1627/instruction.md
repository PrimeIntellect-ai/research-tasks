You are acting as a localization engineer. You have received translation files from different regional teams, but they are in different character encodings and inconsistent formats. Your task is to process these files, extract the relevant data, merge them, and compute a rolling statistic.

Setup:
The files are located in `/home/user/loc_data/`.
1. `en_master.csv` (UTF-8 encoding): Contains the master English keys and strings. Format: `Key,English`
2. `fr_fr.txt` (ISO-8859-1 encoding): Contains French translations. Format: `[KEY] = "Translation"`
3. `es_es.txt` (UTF-16LE encoding): Contains Spanish translations. Format: `Key: KEY | Val: "Translation"`

Your goal is to write a bash script at `/home/user/process_loc.sh` (make sure it is executable) that performs the following steps when run:

1. **Character Encoding & Extraction**:
   - Convert `fr_fr.txt` from ISO-8859-1 to UTF-8. Extract the keys and translation values using regex.
   - Convert `es_es.txt` from UTF-16LE to UTF-8. Extract the keys and translation values using regex.

2. **Merging**:
   - Merge the translations with the master English file based on the `Key`.
   - Output a single UTF-8 encoded CSV file at `/home/user/output/merged_translations.csv`.
   - The output must include a header: `Key,EN,FR,ES`.
   - Sort the output alphabetically by `Key`.
   - If a language is missing a translation for a specific key, leave its column empty. 
   - Ensure the extracted strings do not contain the surrounding quotes from the raw files.

3. **Rolling Statistics**:
   - Calculate the sum of the lengths of the French and Spanish translated strings for each key (if missing, length is 0).
   - Compute a rolling average of this sum over a window of 3 keys (based on the sorted alphabetical order). For the first two keys, the window size will be 1 and 2 respectively.
   - Round the rolling average to 1 decimal place.
   - Output this statistic to a CSV file at `/home/user/output/stats.csv` with the header `Key,RollingAvg`.

Example of rolling average logic:
If the lengths for five keys are 15, 5, 11, 11, 10:
Key 1: 15 / 1 = 15.0
Key 2: (15 + 5) / 2 = 10.0
Key 3: (15 + 5 + 11) / 3 = 10.3
Key 4: (5 + 11 + 11) / 3 = 9.0
Key 5: (11 + 11 + 10) / 3 = 10.7

Ensure the directories exist, and run your script to generate the final files.