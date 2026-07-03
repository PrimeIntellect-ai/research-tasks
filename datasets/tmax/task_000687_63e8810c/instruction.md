You are tasked with building a real-time CSV data ingestion and aggregation service for a data analyst. 

The analyst is streaming transaction logs containing potentially malformed notes. We have provided a vendored lightweight CSV parsing library located at `/app/tinycsv-1.0`. However, the analyst reported that this library currently fails to compile, and even when forced to compile, it abruptly fails and drops rows whenever it encounters a unicode escape sequence (e.g., `\u2028`) in the text fields.

Your objectives:

1. **Fix the Vendored Library**:
   - Navigate to `/app/tinycsv-1.0`.
   - Identify and fix the perturbation in the `Makefile` so the library compiles successfully into `libtinycsv.a` or `libtinycsv.so`.
   - Identify the parsing bug in the C source code that causes the parser to return an error (and drop the row) when encountering `\u` sequences. Modify it so it treats these sequences as literal characters instead of returning an error.

2. **Build the Aggregation Service**:
   - Write a C program (e.g., in `/home/user/csv_aggregator.c`) that links against your fixed `tinycsv` library.
   - The service must orchestrate a multi-stage pipeline: ingestion, deduplication, and aggregation.
   - **Ingestion (TCP)**: The service must listen on `127.0.0.1:8001` for raw TCP connections. It will receive streaming CSV lines in the format: `transaction_id,timestamp,amount,notes`.
   - **Deduplication**: Implement hash-based deduplication using the `transaction_id` string. If a `transaction_id` has already been processed in the current run, ignore the entire row.
   - **Aggregation**: For each unique, successfully parsed row, extract the `amount` field (as a floating-point number) and add it to a running total. Track the total number of unique transactions.
   - **Metrics Endpoint (HTTP)**: The service must also listen on `127.0.0.1:8002`. When it receives an HTTP `GET /stats` request, it must return a valid `HTTP/1.1 200 OK` response with a JSON body exactly in this format:
     `{"unique_count": <integer>, "total_amount": <float>}`
     *(Format the float to 2 decimal places, e.g., `150.50`)*.

3. **Deployment**:
   - Compile your service and ensure it runs continuously in the background, listening on both ports simultaneously.
   - The automated testing suite will send raw CSV payloads over TCP to port 8001, some containing the problematic unicode escapes and duplicate IDs, and then query port 8002 via HTTP to verify the structured JSON summary statistics.

Constraints:
- Do not use external libraries other than standard C libraries (POSIX sockets, pthread, stdlib, etc.) and the provided `tinycsv`.
- Ensure your background service continues running after you complete the task.