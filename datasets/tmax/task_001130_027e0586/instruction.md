You are a data engineer tasked with validating a new set of ETL pipeline queries. Recently, a critical bug caused severe performance degradation due to implicit cross joins and unpaginated large queries in our system. 

We have collected a corpus of ETL queries. Some are safe ("clean"), and some are dangerous ("evil"). 
The exact business rules for what constitutes an "evil" query vs a "clean" query were recorded during a stakeholder meeting. The recording is available at `/app/requirements.wav`.

Your task is to:
1. Transcribe or listen to `/app/requirements.wav` to understand the exact validation rules. The rules involve specific table joins (and avoiding Cartesian products) and pagination limits.
2. Create a Python script at `/home/user/query_validator.py` that acts as a classifier.
3. The script must take a single command-line argument: the path to a SQL file.
   Usage: `python /home/user/query_validator.py <path_to_sql_file>`
4. The script must analyze the SQL file and determine if it is clean or evil based on the audio requirements.
5. If the query is clean, print exactly "CLEAN" to standard output and exit with status code 0.
6. If the query is evil, print exactly "EVIL" to standard output and exit with status code 1.

You can use any Python libraries (like `sqlglot` or standard regex) to parse the SQL and apply the logic. Note that you may need to install an audio transcription tool (e.g., `whisper`) to extract the requirements from the WAV file.

A verification suite will run your script against a hidden set of clean and evil queries to evaluate your solution. Ensure your script handles edge cases robustly!