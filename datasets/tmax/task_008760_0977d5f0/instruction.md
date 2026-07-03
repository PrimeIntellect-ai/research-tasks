You have recently inherited a financial recovery tool from a former developer. The tool is located in `/home/user/fin_recover`. Its purpose is to parse a partially corrupted journal file at `/home/user/transactions.journal`, extract transaction amounts and fees, calculate the total net value (sum of all amounts minus sum of all fees), and write the result to `/home/user/recovered_total.txt`.

However, the codebase is in a broken state:
1. The project currently fails to compile due to missing dependencies and compiler errors.
2. Even when it builds, the original developer mentioned that the calculations suffer from precision loss, resulting in inaccurate totals for large financial records.

Your task:
1. Fix the compiler and dependency errors in the `/home/user/fin_recover` project.
2. Identify and resolve the precision loss issue in the math implementation. 
3. Run the tool so that it reads `/home/user/transactions.journal` and writes the exact, corrected total net value to `/home/user/recovered_total.txt`, formatted to exactly two decimal places (e.g., `1234.56`).

Do not change the file paths. Use the terminal to make necessary code changes and run the project.