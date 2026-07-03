You are a localization engineer managing translation data. A flaky ETL job frequently produces duplicate records or corrupted translation entries during retries.

We need a Python validation script to act as a gatekeeper in our pipeline. You must write a script at `/home/user/validate_l10n.py` that takes a single JSON file path as a command-line argument. The script should analyze the file and exit with code `0` if the file is perfectly clean, or exit with code `1` if it is corrupted ("evil").

The input JSON files contain a list of translation objects, like this:
```json
[
  {
    "msgid": "button.submit",
    "msgstr": "Soumettre",
    "hash": "b2f4c..."
  },
  ...
]
```

**Validation Rules:**
For a file to be considered "clean" (exit code 0), it must meet **both** of the following conditions:
1. **No Duplicates:** There must be absolutely no duplicate `msgid` values in the array.
2. **Valid Signatures:** Every single object's `hash` must exactly match the MD5 hex digest of the concatenated string: `<msgid><msgstr><SALT>`.

**Obtaining the Salt:**
An image containing the current cryptographic salt is located at `/app/l10n_secret.png`. You must use OCR (e.g., `tesseract`, which is installed on your system) to extract the text from this image. The image contains text in the format `SALT: <actual_secret_salt>`. Use the extracted secret salt (stripped of any surrounding whitespace) to validate the hashes.

Your script will be tested automatically against a corpus of clean and evil files. If it accepts all clean files and rejects all evil files, the pipeline will succeed.