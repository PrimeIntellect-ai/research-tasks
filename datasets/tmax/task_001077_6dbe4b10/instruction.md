You are helping a technical writer automate their documentation workflow. The writer dumps raw markdown notes into a nested directory structure, and you need to write a tool that recursively processes these notes, converts their format, and organizes them.

Your task is to write and execute a Python script at `/home/user/compile_notes.py` that performs the following steps:

1. Recursively traverse the directory `/home/user/raw_notes` and locate all Markdown files (files ending with `.md`). Ignore all other file extensions.
2. For each `.md` file found, read its contents and extract:
   - **title**: The text of the first Level 1 Markdown header (a line starting exactly with `# `). Strip the `# ` and any surrounding whitespace. If the file does not contain a Level 1 header, set the title to `"Unknown"`.
   - **content**: The entire raw string content of the file (including headers).
   - **words**: The total word count of the file's content, calculated by splitting the content by standard whitespace (e.g., using Python's `split()`).
3. Convert this information into a JSON object with the keys `"title"`, `"content"`, and `"words"`.
4. Save the JSON object to a corresponding file in `/home/user/processed_notes`. You MUST preserve the internal directory structure. For example, `/home/user/raw_notes/tech/backend/api.md` should be processed and saved to `/home/user/processed_notes/tech/backend/api.json`. If subdirectories do not exist in the destination, your script must create them.
5. Once your script has processed all files, run it. 
6. Finally, create a log file at `/home/user/files_processed.log` containing the absolute paths of all the `.json` files created in `/home/user/processed_notes`, with one path per line, sorted in alphabetical order.

Make sure your script correctly handles edge cases like empty files or files without headers. You have full access to the terminal to write the script, create necessary output directories, run the script, and generate the final log file.