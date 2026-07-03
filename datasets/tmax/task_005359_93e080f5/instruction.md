You are a localization engineer at a software company. We need to analyze community-contributed translation logs to calculate the "translation expansion ratio" (the character length of the translated text divided by the character length of the source text). 

A dump of recent translation logs has been placed at `/home/user/loc_data/raw_logs.txt`.
You must write a C++ program (e.g., `analyze_loc.cpp`) that reads this file, processes the records, and outputs the statistics.

Here is the format of valid lines in the log:
`[YYYY-MM-DDThh:mm:ssZ] LANG:<lang_code> | SRC:<source_text> | TR:<translated_text>`
Example:
`[2023-10-01T10:00:00Z] LANG:es-ES | SRC:Hello world | TR:Hola mundo`

Your C++ program must perform the following pipeline steps:
1. **Extraction & Validation**: Parse each line to extract the timestamp, language code, source text, and translated text. 
   - A line is considered *malformed* if it does not match the exact structure `[<timestamp>] LANG:<lang> | SRC:<src> | TR:<tr>`.
   - Empty translated text (`TR:`) is valid (it means length 0). Empty source text (`SRC:`) is valid.
   - Any malformed line must be skipped and appended exactly as it appears (including the original newline) to `/home/user/loc_data/error.log`.
2. **Sorting & Grouping**: Group the valid translations by their language code (`<lang_code>`). Sort the translations within each language group strictly chronologically by their timestamp.
3. **Rolling Statistics**: For each language group, calculate a rolling average of the translation expansion ratio `(length of TR) / (length of SRC)`. 
   - Use the character count (assume standard ASCII text for this task).
   - If the source text length is 0, the ratio for that specific translation is considered 0.0.
   - The rolling window size is `3` translations. This means the final rolling average is the arithmetic mean of the expansion ratios of the *last 3 chronological translations* for that language.
   - If a language has fewer than 3 total valid translations, the average is computed over however many translations are available.
4. **Output**: Output a JSON file to `/home/user/loc_data/stats.json` containing the final rolling average for each language group. Format it as a simple JSON object where keys are language codes (sorted alphabetically) and values are the averages rounded to exactly 4 decimal places.

Example `stats.json` format:
```json
{
  "es-ES": 0.8125,
  "fr-FR": 1.1500
}
```

Constraints & Environment:
- The input file is large; your solution must group and sort efficiently.
- You have `g++` available (C++17 is recommended: `g++ -std=c++17 analyze_loc.cpp -o analyze_loc`).
- Create the `/home/user/loc_data/` directory and run your code to produce `error.log` and `stats.json`.