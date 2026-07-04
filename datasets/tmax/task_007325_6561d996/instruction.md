You are an automation specialist setting up a data processing pipeline. You have a raw data file at `/home/user/data.txt` containing user session metrics in a wide, pipe-separated (`|`) format. 

You need to write a C program, `/home/user/process.c`, that reads this data from standard input (stdin) and writes the transformed data to standard output (stdout) in a long format. The program should also write execution logs to standard error (stderr).

The input file `/home/user/data.txt` has the following header and structure:
`user_id|email|score_A|score_B|text_A|text_B`

Your C program must perform the following operations:
1. **Wide-to-long reshaping:** For each input row, create up to two output rows (one for type `A` and one for type `B`). If a score column (e.g., `score_B`) is empty, skip generating the row for that type entirely.
2. **Data masking (Anonymization):** Mask the email address. Keep the first two characters of the part before the `@` symbol, and replace the rest of the characters before the `@` with exactly three asterisks (`***`). Keep the domain part as is. (e.g., `john.doe@test.com` becomes `jo***@test.com`, and `ab@test.com` becomes `ab***@test.com`).
3. **Normalization:** Divide the score by 100 and output it formatted to 2 decimal places (e.g., `50` becomes `0.50`).
4. **Tokenization/Standardization:** Convert the text field to lowercase and replace all spaces with underscores `_`.
5. **Logging:** For every data line read (excluding the header), print `LOG: Processed line <N>` to standard error (stderr), where `<N>` starts at 1 for the first data row.

The output must be pipe-separated (`|`) with the following header:
`user_id|masked_email|type|norm_score|tokens`

Compile your C program into an executable at `/home/user/process`.
Then, run the pipeline such that it reads from `/home/user/data.txt`, outputs the processed data to `/home/user/processed.txt`, and redirects the standard error logs to `/home/user/process.log`.