You are a data analyst maintaining a downstream reporting pipeline. An upstream ETL service emits system metrics as a continuous CSV stream over a TCP connection. However, due to a known bug where the ETL job retries on partial failures, the stream sometimes sends duplicate records (identical `id`).

Your task is to write a C program that connects to this service, extracts the relevant features, filters out the duplicates, computes a rolling statistic, and saves the cleaned dataset.

Here are the specific requirements:
1. The upstream service is running locally on TCP port `8080`.
2. Write a C program at `/home/user/process.c` that connects to `localhost:8080` and reads the incoming CSV data until the connection is closed by the server.
3. The incoming data format is: `id,timestamp,cpu,memory\n` (e.g., `1,1677001000,50.0,1024\n`). Note: There is NO header row in the incoming stream. `id` is an integer, `timestamp` is a long integer, `cpu` is a float, and `memory` is an integer.
4. Ignore any record if its `id` has already been processed (deduplication).
5. For each unique record, calculate the rolling average of the `cpu` feature over the **last 3 unique records** (including the current one). For the first and second unique records, the rolling average should be calculated over the 1 and 2 available records, respectively.
6. Your C program must write the results to `/home/user/clean_stats.csv`. 
7. The output file MUST have a header row: `id,rolling_cpu\n`.
8. The `rolling_cpu` values in the output must be formatted to exactly two decimal places (e.g., `55.00`).
9. Compile and run your program so that the final output file is generated correctly.

Do not use any external C libraries other than the standard library (`stdio.h`, `stdlib.h`, `string.h`, `unistd.h`, `sys/socket.h`, `arpa/inet.h`, etc.).