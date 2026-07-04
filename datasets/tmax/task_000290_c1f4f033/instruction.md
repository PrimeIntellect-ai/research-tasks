You are a data engineer building a high-performance ETL pipeline in C++ to process and reshape streaming financial tick data.

We have provided a vendored, header-only CSV parsing library located at `/app/vendor/csv_lib/csv.h`. Unfortunately, the library has a deliberate bug introduced by a previous developer (a missing include or broken macro) that prevents it from compiling. 

Your task is to:
1. Fix the vendored CSV library in `/app/vendor/csv_lib/csv.h`.
2. Write a C++ program at `/home/user/etl_processor.cpp` that streams a large wide-format CSV file provided as the first command-line argument.
3. The input CSV has a header row: `timestamp, SYM1_price, SYM1_vol, SYM2_price, SYM2_vol, ...` containing multiple symbols.
4. **Validation (Adversarial filtering):** As you stream the file, you must validate the character encoding of the data. If you detect ANY invalid UTF-8 sequences or null bytes (`\0`) anywhere in the file's content, your program must immediately:
   - Print `REJECTED` to standard error.
   - Append `ERROR: Invalid encoding in file <filepath>` to `/home/user/pipeline.log`.
   - Exit with return code `1`.
5. **Reshaping & Aggregation:** For clean files, reshape the wide format into a long format. For every symbol, emit a row: `timestamp, symbol, price, vol, rolling_avg_price`.
   - `rolling_avg_price` is a 3-tick simple moving average of the `price` for that specific symbol, up to and including the current timestamp. If fewer than 3 ticks exist for a symbol, average the available ticks.
6. **Output:** Print the long-format CSV to standard output with the header `timestamp,symbol,price,vol,rolling_avg_price`. Records should be output in the order they are read, grouped by symbol in the order they appeared in the wide columns (e.g. SYM1 then SYM2 for row 1, SYM1 then SYM2 for row 2).
7. Compile your program to `/home/user/etl_processor` using `g++ -O3 -std=c++17`.

An automated verifier will test your compiled `/home/user/etl_processor` against two corpora:
- `/app/corpus/clean/`: Contains perfectly well-formed UTF-8 CSVs. Your program must exit with code 0 and output the correctly reshaped/aggregated CSV.
- `/app/corpus/evil/`: Contains CSVs with subtle invalid UTF-8 bytes or null bytes. Your program must exit with code 1, print `REJECTED` to stderr, and log the error.

You must ensure that 100% of the evil corpus is rejected and 100% of the clean corpus is processed successfully.