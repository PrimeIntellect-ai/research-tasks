You are an AI assistant helping a biomedical researcher organize and clean a massive, messy dataset. 

The lab's strict data retention and sanitization rules are unfortunately only available as a scanned image, located at `/app/dataset_rules.png`.

Your task is to:
1. Extract the data classification rules from the provided image.
2. Write a Python script at `/home/user/organizer.py` that enforces these rules.

The script must have the following Command Line Interface:
`python3 /home/user/organizer.py <input_file_path> <output_file_path>`

Requirements for `organizer.py`:
- It must read the text from `<input_file_path>`.
- It must evaluate the contents against the rules extracted from the image.
- If the file violates ANY of the rules (it is an "invalid" or "evil" file), the script must exit with status code `1` and MUST NOT create or modify `<output_file_path>`.
- If the file adheres to all rules (it is a "clean" file), the script must copy its exact contents to `<output_file_path>` and exit with status code `0`.
- To prevent data corruption during massive parallel processing, the writing of the valid file MUST be atomic. You must write to a temporary file first (in the same directory as the target) and then safely move/replace it to the final `<output_file_path>` using filesystem path manipulation (`os.replace` or similar).

Note: You can use `tesseract` to read the image if necessary, as it is preinstalled. Make sure your script handles text files correctly and implements the atomic write pattern flawlessly. We will test your script against a hidden set of clean and malicious files to verify its accuracy.