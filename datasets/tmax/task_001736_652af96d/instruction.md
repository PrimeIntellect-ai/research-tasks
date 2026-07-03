You are a localization engineer tasked with auditing a new build of our application. We have a reference glossary of our English-to-French UI strings. A QA tester has provided a screenshot of the application's debug view, which lists the currently rendered UI keys and their French translations.

Your task:
1. Extract the rendered text from `/app/ui_screenshot.png` using OCR (e.g., Tesseract). The text in the image is formatted strictly as `KEY: Translated String` (one per line).
2. Clean and extract the structured data from the OCR output.
3. Read the reference database at `/app/reference_db.csv`, which contains `key,english,french_expected`.
4. Join/merge the extracted OCR data with the reference data using the `key`.
5. Compute the exact Levenshtein distance between the OCR-extracted translation and the `french_expected` string for each key.
6. Create a stratified sample for an audit report: log the 2 keys with the highest Levenshtein distance (worst translations/OCR errors) and the 2 keys with the lowest distance (perfect or near-perfect matches) into `/home/user/audit_log.txt`. Format it as:
   `WORST: <key1>, <key2>`
   `BEST: <key3>, <key4>`
   (If there are ties, you may pick any valid keys).
7. Calculate the mean Levenshtein distance across *all* matched keys. Save this value as a JSON object in `/home/user/metrics.json` in the exact format:
   `{"mean_distance": 0.75}`

Note: You can use any language (Python is recommended, `pytesseract` and `python-Levenshtein` or similar libraries are generally available or easily installable). Be mindful of typical OCR artifacts like missing accents or dropped punctuation. Do not manually hardcode the distances; write a script that processes the pipeline end-to-end.