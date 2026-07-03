You are helping a developer organize and archive project logs. Over time, the application has generated several JSON-lines (`.jsonl`) log files scattered across various module directories. We need to chunk these files to prepare them for a legacy archiving system.

The project data is located in `/home/user/project_logs`. Inside this directory, there are several subdirectories representing different modules.

Each module directory contains two important files:
1. `data.jsonl`: A file where each line is a valid JSON object.
2. `settings.xml`: An XML configuration file containing archiving rules. 

Your task is to write and execute a Python script to do the following:
1. Recursively traverse `/home/user/project_logs` to find all module directories.
2. For each module directory, parse the `settings.xml` file. Find the `<chunk_lines>` element inside the `<config>` root element to determine the maximum number of lines per chunk.
3. Split the `data.jsonl` file in that directory into smaller files named `data_chunk_0.jsonl`, `data_chunk_1.jsonl`, `data_chunk_2.jsonl`, etc. Each chunk should contain at most the number of lines specified by `chunk_lines`. The chunks must be saved in the same module directory.
4. Generate a summary CSV file at `/home/user/split_summary.csv` containing the results of your operations. The CSV must have the following header exactly:
   `module_dir_name,total_lines,chunk_size,num_chunks`
5. The rows in the CSV should be sorted alphabetically by the `module_dir_name`.

For example, if a module named `api_gateway` has a `data.jsonl` with 250 lines and its `settings.xml` specifies `<chunk_lines>100</chunk_lines>`, you should create `data_chunk_0.jsonl` (100 lines), `data_chunk_1.jsonl` (100 lines), and `data_chunk_2.jsonl` (50 lines). The summary CSV would contain a row: `api_gateway,250,100,3`.

Ensure your Python script completely fulfills all these requirements and is executed to generate the files.