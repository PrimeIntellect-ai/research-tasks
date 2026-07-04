You are a data analyst tasked with preparing a large customer dataset for database import. The company has a strict data anonymization policy. 

You have been provided with a proprietary, stripped Linux binary at `/app/csv_processor_oracle` that implements the company's exact anonymization and hashing logic. However, this binary is deprecated, unoptimized, and we have lost its source code. We need a fast, modern C++ replacement that we can integrate into our parallel data processing pipelines.

Your task is to:
1. Reverse-engineer or black-box test the `/app/csv_processor_oracle` binary to determine its exact text processing, masking, and deduplication hashing rules. The binary reads a single CSV line from standard input in the format: `id,first_name,last_name,email,phone_number` and prints the transformed line to standard output.
2. Write a C++ program at `/home/user/csv_processor.cpp` that perfectly replicates this transformation logic.
3. Compile your program to an executable at `/home/user/csv_processor`.
4. Ensure your C++ implementation is robust and processes standard input to standard output exactly like the oracle.

Your compiled executable `/home/user/csv_processor` will be aggressively fuzzed against the oracle with thousands of randomly generated inputs to ensure bit-exact equivalence. Pay close attention to how the oracle masks emails, formats phone numbers, reorders fields, and generates hashes. 

Please build your executable with `g++ -O3 -std=c++17 /home/user/csv_processor.cpp -o /home/user/csv_processor` (and include any necessary cryptographic libraries if you discover the oracle uses standard hashes).