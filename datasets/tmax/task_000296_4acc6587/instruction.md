You are a support engineer investigating a bug in a C++ trade aggregation service.
We captured a sample of the network traffic, `capture.pcap`, which contains UDP packets sent to port 9000. The payload of each UDP packet represents a trade and is expected to have the following binary format (Little Endian):
- Bytes 0-3: Ticker symbol (4 ASCII characters, padded with null bytes if necessary)
- Bytes 4-7: Sequence number (unsigned 32-bit integer)
- Bytes 8-15: Trade amount (64-bit double precision float)

Customers are reporting two major issues:
1. **Precision Loss**: Query results for highly traded symbols are slightly off. E.g., summing `10000000.0` and two `0.25` trades yields `10000000.0` instead of `10000000.5` in the current implementation.
2. **Crash/Garbage Data on Corrupted Inputs**: Some packets on the network are truncated and missing the `amount` field, resulting in garbage data being read or crashes. 

We have provided the initial buggy code in `/home/user/trade_aggregator.cpp` and a list of requested tickers in `/home/user/queries.txt`.

Your task:
1. Fix the precision loss issue in `trade_aggregator.cpp`.
2. Add handling for corrupted inputs: if a UDP payload is less than 16 bytes, DO NOT process its trade amount. Instead, trace this intermediate state by appending its sequence number to `/home/user/corrupted_seq.log` (one sequence number per line).
3. Update the program to read the requested ticker symbols from `/home/user/queries.txt` (one symbol per line) and output the final summed trade amount for each requested symbol to `/home/user/results.log` in the format `SYMBOL: SUM`.
4. Compile your fixed program using `g++ -o trade_aggregator trade_aggregator.cpp -lpcap` and run it.

Ensure both `/home/user/corrupted_seq.log` and `/home/user/results.log` are correct and present.