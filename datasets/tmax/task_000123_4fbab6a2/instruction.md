You are a storage administrator managing disk space on a heavily utilized server. You need to identify large, obsolete log files from a continuously updating CSV manifest and output their paths in a structured JSON format so that a downstream automated archiving service can process them.

A previous engineer started building a fast C++ utility for this, located at `/home/user/src/manifest_filter.cpp`, which relies on a vendored package located at `/app/vendored/csv_parser`. However, the vendored package is currently failing to compile due to a known issue, and the utility itself is incomplete.

Your task is to:
1. Fix the compilation issue in the vendored package at `/app/vendored/csv_parser`.
2. Complete the C++ program at `/home/user/src/manifest_filter.cpp` and compile it to an executable named `/home/user/src/manifest_filter`.

Program specifications:
- The program must read CSV data from `stdin`. The CSV format is `filename,size_bytes,file_type` (without a header).
- It must filter the rows to keep only those where `file_type` is exactly `"log"` AND `size_bytes` is strictly greater than `10485760` (10 MB).
- It must output a valid JSON array containing just the `filename` strings of the matching rows to `stdout`.
- Example input:
  ```csv
  /var/log/syslog,15000000,log
  /var/log/auth.log,5000000,log
  /opt/data.db,100000000,db
  /var/log/old.log,20000000,log
  ```
- Example output:
  ```json
  [
    "/var/log/syslog",
    "/var/log/old.log"
  ]
  ```
- Ensure you use standard C++ constructs. You may link against the fixed `/app/vendored/csv_parser` if needed, or simply use standard libraries, but the final executable must be located at `/home/user/src/manifest_filter`.

Test your executable to ensure it behaves correctly, as an automated test will rigorously evaluate it against a reference implementation using varied inputs.