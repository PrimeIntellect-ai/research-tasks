You are a data analyst working on consolidating customer records from two sources: an automated legacy system that outputs noisy CSVs, and a voice-dictated log from field agents. 

We have provided two input files:
1. `/app/legacy_records.csv`: A CSV file containing existing customer records. The file is messy and contains invalid entries.
2. `/app/field_dictation.wav`: An audio recording of a field agent dictating new customer records (names, cities, and ages).

Your task is to build a robust C++ data processing pipeline that does the following:

**Step 1: Audio Transcription**
Use any available command-line tool (e.g., whisper) to transcribe `/app/field_dictation.wav`. The audio contains dictated records with international names. Save the raw transcript to `/home/user/transcript.txt`.

**Step 2: C++ Data Processor**
Write a C++ program at `/home/user/processor.cpp` and compile it to `/home/user/processor`. The program must:
* Read `/home/user/transcript.txt` and extract the dictated records. The dictation follows a predictable pattern but requires tokenization.
* Read `/app/legacy_records.csv`.
* Implement constraint-based data validation: Discard any records (from either source) where the age is less than 18 or greater than 120, or where the city name contains numbers.
* Handle multi-language text properly: Ensure UTF-8 characters in names and cities are preserved without corruption during tokenization.
* Implement pipeline logging: For every record discarded due to validation constraints, append a log entry to `/home/user/pipeline.log` in the format: `REJECTED: [Reason] - [Raw Record Text]`.
* Output the valid, merged records to `/home/user/clean_merged.csv` in the exact format: `Name,City,Age`.

**Requirements:**
* Compile your C++ program using g++ with standard libraries (C++17 is available).
* The final `/home/user/clean_merged.csv` must contain a header row `Name,City,Age` followed by the valid records.

Your final output will be evaluated by an automated script that computes the Record Matching Accuracy (F1-score) of your `clean_merged.csv` against a hidden ground-truth dataset. You must achieve an accuracy score of at least 0.90 to pass.