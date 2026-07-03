You are tasked with fixing and securing a data analytics ingestion pipeline. 

Currently, our pipeline receives CSV files over a raw TCP socket, performs a basic similarity search, and forwards the data to a Redis backend. However, malicious actors are sending malformed data (adversarial numerical anomalies and out-of-bound values) that crash our downstream numerical libraries.

Your tasks are:
1. **Develop a CSV Sanitizer in C**: Write a C program at `/home/user/sanitizer.c` and compile it to `/home/user/sanitizer`. The program must read CSV data from standard input. A valid row has exactly 4 columns: `id` (integer), `feature1` (float), `feature2` (float), and `category` (string, max 10 chars). 
   Your sanitizer MUST silently drop any row that:
   - Does not have exactly 4 columns.
   - Contains non-numeric characters in the `feature1` or `feature2` fields (other than a single decimal point or a leading minus sign).
   - Has `feature1` or `feature2` values outside the range [-1000.0, 1000.0].
   - Has a `category` string longer than 10 characters.
   The program must output only the valid rows to standard output.

2. **Reconfigure the Services**: We have a multi-service setup managed by `/app/start_pipeline.sh`. The file currently contains stubbed commands. You need to modify `/app/start_pipeline.sh` so it ties the services together:
   - Start a Redis server in the background on the default port (6379).
   - Start a TCP listener on port 9000 using `nc` (netcat).
   - Every time a connection is made to port 9000, pipe the incoming data through your compiled `/home/user/sanitizer`, and append the clean output to a Redis list named `clean_data` using `redis-cli -x rpush clean_data`. (Hint: use a bash `while` loop or `ncat` with an exec script if available, but keep it simple with standard tools).

We will verify your solution by compiling your C code and pumping a large set of both clean and evil CSV files through your pipeline on port 9000.