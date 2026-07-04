You are a storage administrator managing disk space on a heavily utilized server. There is a directory containing compressed JSON log files located at `/home/user/log_dumps/`. To free up space and catalogue archived data, you need to identify which logs are marked as "ARCHIVED" and generate a report, directly processing the compressed streams to avoid filling up the remaining disk space with uncompressed data.

Your task is to write a C++ program (and use any necessary shell commands) to do the following:
1. Iterate through all `.gz` files in `/home/user/log_dumps/`.
2. Read and uncompress each file's contents directly into memory (you must not extract the files to disk).
3. Parse the uncompressed JSON data. The JSON has the structure: `{"node_id": "...", "status": "...", "metrics": {"total_size": ...}}`.
4. If the `status` field is exactly `"ARCHIVED"`:
   a. Record the file's original name and its `metrics.total_size` value into a CSV report located at `/home/user/archive_report.csv`. The CSV should have the header `filename,total_size` and be sorted alphabetically by filename.
   b. Rename the processed `.gz` file by appending `.processed` to its filename (e.g., `nodeX.json.gz` becomes `nodeX.json.gz.processed`).
5. If the `status` field is anything else (e.g., `"ACTIVE"`), do not add it to the report and do not rename the file.

Environment details:
- You have `g++`, `zlib1g-dev`, and the nlohmann-json library (`nlohmann-json3-dev`) installed.
- You can include the JSON library via `#include <nlohmann/json.hpp>`.
- You can compile your C++ code anywhere in `/home/user/`.