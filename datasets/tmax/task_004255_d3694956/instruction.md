You are a log analyst investigating anomalies in a high-throughput microservice architecture. 

We have a legacy, single-threaded log aggregator tool located at `/app/bucket_oracle`. This tool processes JSON log files and outputs a time-bucketed aggregation. However, it is far too slow to handle our daily volume.

Your task is to write a highly optimized, parallelized Go program at `/home/user/parallel_processor.go` that perfectly replicates the logic of the oracle but runs significantly faster. 

Here is what you know:
1. There is a large test log file located at `/home/user/requests.log`.
2. The legacy tool `/app/bucket_oracle` can be run as `/app/bucket_oracle <input_file> <output_csv_file>`. It is a stripped binary.
3. Your Go program must take the exact same arguments: `go run parallel_processor.go <input_file> <output_csv_file>`.
4. Your output CSV must perfectly match the output of the oracle (including the header, and sorted identically: first by time window, then by endpoint alphabetically).
5. You must implement parallel data processing (e.g., worker pools, chunked reading) to achieve the performance requirements.
6. Your program must include basic pipeline logging to stdout (e.g., "Processed 100000 lines...").

To figure out the exact aggregation rules (time bucket size, percentile calculations, error counting logic), you should create small, synthetic JSON log files, feed them to `/app/bucket_oracle`, and observe the output. 

Your final goal is to produce `/home/user/summary.csv` using your Go program, ensuring the data exactly matches what the oracle would produce, but completing the execution with at least a **3.0x speedup** compared to the oracle.