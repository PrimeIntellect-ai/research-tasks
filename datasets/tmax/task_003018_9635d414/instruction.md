You are a Database Reliability Engineer handling a severe ransomware incident. The attackers corrupted several of our raw JSONL backup streams. They injected malformed rows with invalid schemas, and structurally corrupted self-referencing tables by creating cyclic foreign-key relationships (which will crash our recursive SQL restore queries).

We must filter these backup streams before ingestion.

We lost the original schema documentation, but we managed to salvage a screen recording of the database terminal during the last schema migration: `/app/schema_recording.mp4`. 

Your objectives:
1. Extract and analyze the frames from `/app/schema_recording.mp4` to recover the exact allowed table names, their columns, and which columns are self-referencing foreign keys.
2. Write a C program that validates backup files. The program must be written in C and compiled to `/home/user/filter_backup`.
3. The program must accept a single command-line argument: the path to a `.jsonl` backup file.
4. Each line in the backup file is a JSON object representing a database row. It includes a `_table` key indicating the table name.
5. Your C program must read the file and determine if it is completely valid. It must print exactly `ACCEPT` to standard output (with a newline) and exit with code 0 if:
   - Every JSON object strictly matches the columns defined for its table in the video (no extra columns, no missing columns, excluding the internal `_table` key).
   - There are absolutely NO cyclic dependencies in the self-referencing tables (e.g., no recursive loops where A is a child of B, and B is a child of A).
6. If the file violates any schema rules or contains cycle-inducing data, your program must print exactly `REJECT` and exit with code 1.

You have access to a standard Linux environment. You may install C JSON libraries (like `libjansson-dev` or `libcjson-dev`), `ffmpeg`, and OCR tools (like `tesseract-ocr`) to help with frame analysis.

Ensure your compiled executable is robust. It will be tested against a hidden suite of clean and corrupted backup files to verify your schema validation and cycle-detection logic.