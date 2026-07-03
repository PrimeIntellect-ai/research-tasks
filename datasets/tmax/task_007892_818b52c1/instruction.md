You are a localization engineer working on a highly technical mathematics video course. The video editing team recently changed the framerate and added an intro bumper to the raw video, which caused all the existing subtitle translations to fall out of sync. Furthermore, the analytics team wants to estimate the mathematical complexity of each subtitle block to correlate with student engagement.

Your task is to build a multi-language, parallel data processing pipeline that reads the existing translation files, aligns the timestamps using a mathematical transformation, computes a "math complexity score", and writes the normalized data to a single unified format.

The input files are located in `/home/user/locales/`:
1. `/home/user/locales/en.json` (JSON format)
   Contains an array of objects with `id`, `start`, `end`, and `text`. Timestamps are in `HH:MM:SS.mmm` format.
2. `/home/user/locales/es.xml` (Custom XML format)
   Contains `<sub id="..." start="..." end="...">` elements with `<text>` inside. Timestamps are in raw seconds (e.g., `12.500`).
3. `/home/user/locales/fr.csv` (CSV format)
   Contains columns `id,start,end,text`. Timestamps are in `HH:MM:SS.mmm` format.

You must perform the following operations:
1. **Parallel Processing**: Process the files concurrently using a parallel execution method of your choice (e.g., GNU `parallel`, Bash background jobs, or a multi-processing script).
2. **Timestamp Alignment**: Convert all `start` and `end` timestamps into seconds (float). Then, apply the following mathematical transformation to account for the framerate stretch and the new intro bumper:
   `new_time = (old_time_in_seconds * 1.05) + 1.25`
   Round the resulting `new_time` to exactly 3 decimal places.
3. **Math Complexity Score**: For each subtitle's `text`, calculate an integer score representing the number of mathematical characters. The score is the total count of the following characters present in the string: `+`, `-`, `=`, `^`, `_`, `\` (backslash).
4. **Data Normalization**: Output the processed data into a single JSONL file at `/home/user/aligned_subs.jsonl`. Each line must be a valid JSON object with the following keys:
   - `lang`: The language code (`en`, `es`, or `fr`), derived from the filename.
   - `id`: The subtitle ID as an integer.
   - `start_adj`: The adjusted start time (float).
   - `end_adj`: The adjusted end time (float).
   - `math_score`: The calculated integer score.

**Final Sorting Requirement**:
To ensure the output is strictly verifiable, after your parallel jobs complete, sort the final `/home/user/aligned_subs.jsonl` file by `id` ascending, and then by `lang` ascending (alphabetical order). 

Ensure you use proper system tools and scripts. You may install standard packages via `apt` or `pip` if necessary.