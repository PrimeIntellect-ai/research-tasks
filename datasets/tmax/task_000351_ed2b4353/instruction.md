You are a data analyst at a retail analytics firm. Your manager has left you an audio voicemail at `/app/voicemail.wav` containing instructions for a new ad-hoc reporting tool they need immediately. 

In the `/home/user/data/` directory, you will find three CSV files:
- `users.csv`
- `transactions.csv`
- `products.csv`

Your task is to:
1. Listen to or transcribe the voicemail at `/app/voicemail.wav` to understand the implicit data model, the relationships between the CSV files, and the exact aggregation logic your manager is requesting. You may install any command-line tools you need (like `ffmpeg`, `whisper`, etc.) to process the audio.
2. Reverse engineer the CSV schemas to match the verbal instructions.
3. Write a C++ program that implements the requested parameterized query and cross-query aggregation over the CSV files. 
4. The C++ program must execute efficiently, perform output schema validation, and print the results to standard output in the exact format requested in the voicemail.
5. Compile your C++ program to an executable located exactly at `/home/user/query_engine`. 

Ensure your executable can take the parameters specified in the audio, processes the CSVs from `/home/user/data/`, and outputs the correct aggregated records to `stdout`. Automated testing will run your executable with various inputs to ensure it is perfectly equivalent to the reference implementation.