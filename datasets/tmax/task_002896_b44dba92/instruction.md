You are acting as a systems data analyst. We have received two CSV files containing market data: `/home/user/quotes.csv` and `/home/user/trades.csv`. 

Your task is to write a highly efficient C program that processes these files to compute the Volume-Weighted Average Spread (VWAS) for each traded symbol.

Here are the requirements:
1. Write a C program at `/home/user/processor.c`.
2. The program must read both CSV files.
   - `quotes.csv` format: `timestamp,symbol,bid,ask`
   - `trades.csv` format: `timestamp,symbol,price,volume`
   - Timestamps are in ISO8601 format: `YYYY-MM-DDTHH:MM:SSZ`.
3. For each trade in `trades.csv`, your program must:
   - Find the most recent quote for the *same symbol* from `quotes.csv` where `quote.timestamp <= trade.timestamp`. (Assume both files are chronologically sorted, but symbols are interleaved).
   - If no preceding quote exists for a symbol, ignore the trade.
   - Calculate the "spread" at the time of the trade: `spread = ask - bid`.
4. Calculate the Volume-Weighted Average Spread for each symbol: `sum(spread * volume) / sum(volume)`.
5. Your program must output the final results to `/home/user/vwas_report.csv`.
   - The output must have the header: `symbol,vwas`
   - The `vwas` values must be formatted to exactly 4 decimal places (e.g., `0.0800`).
   - The output rows must be grouped by symbol and sorted alphabetically by symbol.
6. Compile your program to `/home/user/processor` using `gcc` and standard libraries only.
7. Run the program to generate the `/home/user/vwas_report.csv` file.

Both CSV files are guaranteed to fit in memory (for the scope of this test), but you must properly parse the timestamps and merge the datasets.