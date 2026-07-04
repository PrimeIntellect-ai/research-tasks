You are tasked with building a robust configuration ingestion pipeline. Our ETL job pulls YAML and JSON configuration files from edge devices, but due to network retries, it frequently produces duplicate records. Furthermore, a recent security audit revealed that some configurations contain injected malicious directives or accidentally leaked cleartext passwords.

Your goal is to build a configuration manager that filters these out using a DAG orchestration approach.

Here are your instructions:

1. **Fix the Parsing Tool**: We use `yq` (the Python-based wrapper around `jq`) to validate configurations, but the vendored source code at `/app/yq` is currently broken due to a recent bad commit. Identify the bug (a deliberate syntax/import perturbation), fix it, and install the package locally so `yq` is available in your PATH.

2. **Create the Ingestion Script**: Write a Bash script at `/home/user/process_configs.sh` with the following signature:
   `bash /home/user/process_configs.sh <input_dir> <output_dir>`

3. **Pipeline DAG Orchestration**: Your Bash script must not process the files sequentially in a loop. Instead, it must dynamically generate a `Makefile` that represents the processing tasks as a Directed Acyclic Graph (DAG) and then invoke `make -j4` to process the configurations in parallel. 

4. **Processing Rules (The DAG's tasks)**:
   For each file in `<input_dir>`, the pipeline must apply the following logic:
   * **Hash-based Deduplication**: Compute the SHA256 hash of the file. If multiple files in the input directory have the exact same contents, only the file with the lexicographically earliest filename should be kept; the rest must be rejected.
   * **Regex Pattern Construction**: The file must be rejected if it matches *either* of these regex patterns:
     a) An injected evil directive: the exact string `evil_directive:` followed immediately by one or more non-whitespace characters.
     b) A cleartext password leak: the string `password:` followed by optional whitespace and a sequence of strictly alphanumeric characters `[a-zA-Z0-9]` to the end of the line.

5. **Output**: Files that pass all checks (unique and non-malicious) must be copied to `<output_dir>` with their original filenames.

To test your solution, two directories are provided:
- `/app/corpus/clean/`: Contains valid, unique configuration files. Your script must copy 100% of these to the output directory.
- `/app/corpus/evil/`: Contains malformed configs (duplicates of clean files, or files containing forbidden regex patterns). Your script must reject 100% of these (the output directory should be empty if run solely on this corpus).

Ensure your script is executable and completely automated. Do not hardcode the names of the files in your script.