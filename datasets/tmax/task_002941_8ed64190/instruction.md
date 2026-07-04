You are a support engineer tasked with investigating a critical bug reported by a client. The client uses our custom C++ transaction processing tool to aggregate daily financial data. Recently, they noticed subtle discrepancies between the tool's output and their internal accounting systems. 

You have been given a workspace in `/home/user/` containing:
1. `/home/user/parser.cpp`: The source code of the transaction parser.
2. `/home/user/transactions.txt`: A large log file (10,000 lines) of yesterday's transactions provided by the client.
3. `/home/user/expected_sum.txt`: The exact mathematical sum the client expects for the file.

The client's system runs this parser, and currently, the output does not match `expected_sum.txt` due to a precision loss issue combined with a format parsing edge-case.

Your objectives:
1. **Delta Debugging & MRE Creation**: The 10,000-line input is too large to debug manually. Create a script or use bisection techniques to isolate the exact minimal reproducible example (MRE). Find the **single line** from `transactions.txt` that triggers the precision loss bug. Save this exact single line to `/home/user/mre.txt`.
2. **Error Diagnosis & Fix**: Analyze `/home/user/parser.cpp`. Identify where the precision loss and format parsing edge-case occurs. Fix the C++ source code so it retains full precision for all transaction types.
3. **Build**: Compile your fixed code using: `g++ -O2 /home/user/parser.cpp -o /home/user/parser_fixed`.
4. **Verification**: Run your fixed parser on the original `/home/user/transactions.txt`. Save the stdout (which should just be the final total sum, formatted to 4 decimal places) to `/home/user/final_sum.txt`.

Ensure all requested files (`mre.txt`, `parser_fixed`, `final_sum.txt`) are precisely located in `/home/user/`.