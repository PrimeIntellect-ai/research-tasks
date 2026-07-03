You are a data scientist debugging a broken ETL pipeline. Due to a recent retry bug, your daily feedback logs contain duplicate entries. Furthermore, the pipeline is missing its required data masking and text normalization steps. 

You need to write a C program that reads a raw pipe-separated (`|`) log file, cleans it, and writes the results to a new file.

**Input File:** `/home/user/raw_feedback.txt`
The file has no header. Each line is formatted as:
`timestamp|user_id|email|feedback_text`

**Requirements for the C program:**
1. **Text Normalization:** Convert the `feedback_text` to strictly lowercase and remove all punctuation (any character that is not a lowercase-letter, digit, or space). Do not remove spaces.
2. **Data Masking:** Anonymize the `email` field by replacing everything before the `@` symbol with exactly three asterisks (`***`). For example, `john.doe@example.com` becomes `***@example.com`.
3. **Hash-Based Deduplication:** Some records are duplicates due to the ETL retry bug, or users submitting slight variations of the same text (differing only by case/punctuation). You must deduplicate records based *only* on the normalized `feedback_text`. If multiple records have the exact same normalized feedback text, keep only the *first* occurrence (based on the order in the input file) and discard the rest. You must implement a simple hash table or hash set in C to track seen normalized texts.
4. **Output Format:** Output the cleaned, deduplicated records to `/home/user/cleaned_feedback.txt` in the exact same format: `timestamp|user_id|masked_email|normalized_feedback_text`. 

**Constraints:**
- Your solution must be written in C. Save your source code to `/home/user/cleaner.c` and compile it to `/home/user/cleaner`.
- Do not use external libraries other than the C standard library.
- The maximum line length in the input will not exceed 1024 characters.
- You may assume there are at most 1000 unique records.

Once you have written, compiled, and executed your C program, ensure `/home/user/cleaned_feedback.txt` exists and contains the correct output.