You are a localization engineer preparing a string translation report. You have been given a JSON file containing UI strings in English and their French translations. Some French translations are missing, and some existing ones might be drastically different in length compared to the English source, which can break the UI layout.

Your task is to process this JSON file using standard Linux command-line tools (like `jq`, `awk`, `sed`, etc.) to clean, impute, analyze, and convert the data into a CSV report.

**Input:**
A JSON file located at `/home/user/locales.json`. It contains an array of objects, each with `id`, `en`, and `fr` keys. If a French translation is missing, the `fr` value will be `null` or an empty string `""`.

**Processing Requirements:**
1. **Imputation**: If the `fr` translation is missing (null or empty), impute it by taking the `en` string and prepending exactly `[FR]` to it (e.g., if English is "Hello", imputed French is "[FR]Hello").
2. **Length Calculation**: Determine the character length of the English string (`len_en`) and the (possibly imputed) French string (`len_fr`).
3. **Rolling Statistics**: Calculate a 3-item rolling average of the `len_fr` values, keeping the order of the JSON array. 
   - For the first item, it's just its own `len_fr`.
   - For the second item, it's the average of the first and second `len_fr`.
   - For the third item onwards, it's the average of the current and previous two `len_fr` values.
   - Format this rolling average to exactly 1 decimal place (e.g., `11.0`, `9.3`).
4. **Distance/Similarity Flagging**: We need to flag translations where the string length deviates too much from the source. Calculate the length distance metric: `abs(len_en - len_fr) / len_en`. If this value is strictly greater than `0.5`, set the `flag` to `1`. Otherwise, set it to `0`.

**Output:**
Create a CSV file at `/home/user/processed_locales.csv` with exactly the following headers:
`id,imputed_fr,fr_len,rolling_avg_3,flag`

*Note: Ensure the CSV does not contain quotes around the fields unless strictly necessary for escaping commas (the input data will not contain commas in the strings to simplify processing).*