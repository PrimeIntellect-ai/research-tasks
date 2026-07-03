I am a researcher organizing some large dataset files. I wrote a fast C-based ETL tool located at `/home/user/etl.c` to parse a CSV file (`/home/user/data.csv`) and filter/clean it, writing the output to `/home/user/data_clean.csv`. 

However, my pipeline reproducibility tests are failing because some of the timestamp values in the output CSV are negative! The original dataset only contains positive timestamps. It seems there is a silent data corruption issue similar to integer overflow happening during the parsing.

Please do the following:
1. Identify and fix the bug in `/home/user/etl.c` so it can properly handle large timestamp values (up to 10^12) without overflowing. 
2. Compile your fixed C program into an executable named `/home/user/etl_fixed`.
3. Run `/home/user/etl_fixed` to process `/home/user/data.csv` and generate the corrected `/home/user/data_clean.csv`.

Ensure the resulting `/home/user/data_clean.csv` accurately reflects the large timestamps from the input without any corruption.