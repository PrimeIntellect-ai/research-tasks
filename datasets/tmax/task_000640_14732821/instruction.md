You are acting as a Database Administrator. A product manager left you a voice message with the requirements for a new critical business report. The audio file is located at `/app/pm_request.wav`. 

Additionally, a junior developer attempted to build this report in Python, located at `/app/naive_report.py`. It runs against the SQLite database at `/app/company_data.db`. However, the junior developer's script uses inefficient N+1 queries and in-memory Python calculations, making it far too slow.

Your task is to:
1. Extract the exact business logic and filtering requirements from the audio file `/app/pm_request.wav`. You may install and use transcription tools (like whisper or ffmpeg) to decode the message.
2. Write a highly optimized Python script at `/home/user/optimized_report.py` that implements the requested logic entirely within the SQL database engine using complex joins and window functions.
3. Your script must connect to `/app/company_data.db`, execute the optimized query, and output the exact same columns and data to `/home/user/report.csv` as the naive script would (if it finished in a reasonable time), but updated to reflect the specific filtering rules mentioned in the audio.

Requirements for `/home/user/optimized_report.py`:
- It must take no arguments and output the file `/home/user/report.csv`.
- Include headers in the CSV.
- Do not use N+1 queries; use a single efficient SQL query.

An automated test will run your script and compare its execution time against the naive implementation, while also checking the data correctness of `report.csv`. You need to achieve a speedup of at least 15x compared to the naive approach.