You are a localization engineer tasked with processing an erratic subtitle log file for a video presentation. The raw log contains timestamps, speakers, and untranslated text. You need to parse this time series data, normalize the text, translate specific terms, and fill in missing timing gaps to create a continuous track.

You must write a C++ program `/home/user/process_subs.cpp` that performs these tasks and produces a final JSON Lines (JSONL) file.

**Input Files (Assume these exist):**
1. `/home/user/subs_raw.log`
   Format: `[HH:MM:SS] [SPEAKER] Text with Punctuation.`
   Example:
   `[00:00:00] [NARRATOR] Hello, world.`
   `[00:00:02] [NARRATOR] Welcome to the tutorial!`
   `[00:00:08] [GUEST] This is exciting.`

2. `/home/user/dict.csv`
   Format: `english_word,localized_word` (all lowercase, no spaces).

**Processing Requirements:**

1. **Regex Parsing & Time Normalization:**
   Read `subs_raw.log`. Use Regex to extract the timestamp, speaker, and text. Convert the `HH:MM:SS` timestamp into an integer representing total seconds from `00:00:00` (this is the `start_sec`).

2. **Text Normalization & Tokenization:**
   For the extracted text:
   - Convert all letters to lowercase.
   - Remove all characters that are NOT alphanumeric and NOT spaces (e.g., remove commas, periods, exclamation marks).
   - Tokenize the text by space. 
   - If a token exactly matches an `english_word` in `dict.csv`, replace it with the `localized_word`.
   - Reconstruct the sentence by joining the tokens with a single space.

3. **Gap-Filling & Resampling (Time Series):**
   You must calculate an `end_sec` for each line and handle long pauses:
   - The default `end_sec` of a line is the `start_sec` of the *next* line.
   - **Gap Rule:** If the duration between a line's `start_sec` and the next line's `start_sec` is strictly greater than `4` seconds, cap the current line's `end_sec` at `start_sec + 3`. 
   - Then, insert a new "gap-fill" record that starts at the capped `end_sec` and ends at the next line's `start_sec`. This gap record must have the speaker `"SYS"` and the text `"[SILENCE]"`.
   - **Final Line Rule:** The very last subtitle in the log should always have its `end_sec` set to its `start_sec + 3` (do not add a trailing silence gap).

4. **Output Format:**
   Write the processed timeline to `/home/user/subs_normalized.jsonl`. Each line must be a valid JSON object with the following keys:
   `{"start_sec": <int>, "end_sec": <int>, "speaker": "<string>", "text": "<string>"}`
   Ensure the keys and values strictly match this format and the records are in chronological order.

Compile your C++ code (e.g., using `g++ -std=c++17 process_subs.cpp -o process_subs`) and execute it to generate the output file.