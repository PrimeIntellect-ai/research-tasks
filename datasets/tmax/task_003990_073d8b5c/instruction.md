You are acting as a localization engineer. We have a legacy C-based ETL pipeline for our translation data that has a critical flaw: our rudimentary CSV parser silently drops or corrupts rows that contain embedded newlines inside quoted strings. Since many of our UI translation templates span multiple lines, this is causing massive data loss. 

Furthermore, we are receiving polluted translation files from a vendor. Some files contain perfectly valid multi-line translations, but others contain anomalous regex injections and malformed template variables that crash our downstream template-generation engine.

Your task is to create a robust C-based localization sanitizer tool. 

Requirements:
1. First, listen to (transcribe) the audio file located at `/app/audio/template_dictation.wav`. It contains a dictation of the exact expected template variable format for our localization strings (e.g., "All variables must be enclosed in..."). You must use this rule to build a regex pattern or parsing logic for anomaly detection.
2. Write a C program, compiled to `/home/user/loc_sanitizer`.
3. The program must take a single command-line argument: the path to a CSV file.
4. The CSV files have the format: `string_id,language_code,translation_text`. 
5. The `translation_text` column often contains quoted strings with embedded newlines. Your parser must correctly read these without dropping rows or misaligning columns.
6. The program must validate the `translation_text`. It must reject the file (exit with code 1) if it finds any anomalous template variables that do not match the rule dictated in the audio file, or if the CSV is structurally malformed (e.g., unclosed quotes).
7. If the file is structurally valid, properly handles all quoted newlines, and all template variables match the standard, the program must exit with code 0.

You will need to install any necessary tools (like `ffmpeg` or transcription tools) to process the audio file. Write your C program to be highly robust against adversarial edge cases. We will test your compiled `/home/user/loc_sanitizer` against a hidden corpus of clean and evil CSV files.