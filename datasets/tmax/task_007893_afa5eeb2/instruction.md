I have a legacy binary data file located at `/home/user/transactions.dat`. As a data analyst, I need to extract successful transactions from this file and convert them into a structured CSV format for downstream processing. 

I don't have the exact C struct definition used to write this file, but I have reverse-engineered the layout. Each record is exactly 25 bytes long and tightly packed (no padding):
- Bytes 0-3: `transaction_id` (unsigned 32-bit integer, little-endian)
- Bytes 4-19: `user_name` (up to 16 bytes, null-terminated ASCII string)
- Bytes 20-23: `amount` (32-bit IEEE 754 floating-point number, little-endian)
- Byte 24: `status` (unsigned 8-bit integer, where `1` indicates a successful transaction, and other values indicate failed or pending)

Please do the following:
1. Write a C program at `/home/user/extract.c` that reads `/home/user/transactions.dat`.
2. The program must parse the tightly packed records and filter for those where `status == 1`.
3. For the successful transactions, output them to `stdout` in CSV format: `transaction_id,user_name,amount` (format the amount to exactly 2 decimal places).
4. Compile your program to an executable named `/home/user/extract`.
5. Run your executable and pipe its output through standard Linux shell commands to transform it. The final pipeline should:
   - Keep only the `transaction_id` and `amount` columns.
   - Add a header row: `id,amount`
   - Sort the data rows numerically by `transaction_id` in ascending order.
   - Save the final output to `/home/user/successful_amounts.csv`.

Ensure your C code accounts for the fact that the 25-byte records are unpadded. The final file `/home/user/successful_amounts.csv` must be strictly validated against the requested schema (header + sorted data).