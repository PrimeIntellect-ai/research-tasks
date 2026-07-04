As a data scientist, I am cleaning a large transaction dataset that got corrupted during a failing ETL job. The ETL job retried multiple times, creating a massive number of duplicate records. Additionally, a small batch of recent records was lost from the database but exists in an audio backup log.

Here is what you need to do:
1. Recover the lost records from the audio backup located at `/app/retry_audio.wav`. This file contains spoken customer records. You can use any standard command-line tool or write a short Python script to transcribe it.
2. Append the transcribed records to the main dataset located at `/app/historical_transactions.csv`. The dataset uses the format: `Name, SSN, TransactionAmount`.
3. Write a C program (`/home/user/clean_data.c`) to process the combined dataset. Your C program MUST:
   - Use multi-threading (e.g., OpenMP or pthreads) to process chunks of the file in parallel.
   - Properly handle multi-language UTF-8 encoded names (e.g., "José", "Müller", "Wei").
   - Mask the SSNs for anonymization, replacing the first 5 digits of any `XXX-XX-XXXX` pattern with asterisks (e.g., `***-**-6789`).
   - Remove duplicate records (the ETL retry issue). If two lines have the same Name, SSN, and Amount, only keep one.
   - Mathematically calculate the sum of all unique `TransactionAmount` values.
4. Compile your C program to `/home/user/clean_data` and run it.
5. The program should output the masked, deduplicated records to `/home/user/cleaned_transactions.csv` and write the final calculated sum to `/home/user/total_sum.txt`.

Our test suite will verify your output for correctness and will measure the execution speed of `/home/user/clean_data` to ensure you successfully implemented parallel data processing. You must achieve a speedup of at least 1.5x over our sequential reference implementation.