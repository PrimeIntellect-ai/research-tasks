You are an analyst tasked with modernizing a legacy data processing workflow. We have a stripped, undocumented binary located at `/app/csv_processor` that performs an aggregation pipeline on CSV files. It takes a single argument: the path to a CSV file.

Your goal is to write a purely Bash-based equivalent (which may use standard Unix tools like `awk`, `sort`, `grep`, `head`, etc.) that replicates the exact behavior and output of the legacy binary.

What we know about the data and the binary:
1. The input CSVs always have the header: `id,department,status,revenue,cost,timestamp`.
2. The binary parses the CSV, performs some filtering, groups the data by department, computes a profit metric (based on revenue and cost) and a count, sorts the results, and paginates/limits the output.
3. The binary formats the output in a specific way.

Your task:
1. Analyze the behavior of `/app/csv_processor` by creating dummy CSV files and observing its outputs.
2. Deduce the exact filtering rules, aggregation math, sorting order, and pagination limit used by the binary.
3. Write a script at `/home/user/process.sh` that takes a CSV file path as its first and only argument.
4. Your script must output the exact same text (byte-for-byte) as `/app/csv_processor` for any valid CSV input matching the schema.

Ensure your script handles edge cases (like no rows matching the filter) the same way the binary does. Make your script executable (`chmod +x /home/user/process.sh`).