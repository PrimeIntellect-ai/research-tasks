You are an AI assistant helping a systems researcher organize a hybrid dataset containing experimental ELF binaries and corresponding CSV metadata. 

The researcher has an automated pipeline that drops compiled ELF binaries into `/home/user/dataset/binaries/`. There is also a metadata file at `/home/user/dataset/metadata.csv` which contains experimental parameters.

Your task is to consolidate this information into a single structured summary file.

Here are the requirements:
1. Parse all ELF binaries in `/home/user/dataset/binaries/`. For each binary, extract the following two fields using the ELF header:
   - The Machine Architecture (e.g., "Advanced Micro Devices X86-64")
   - The Entry point address (e.g., "0x401000" or whatever it is exactly)
2. Read `/home/user/dataset/metadata.csv`. The CSV has the header `filename,experiment_id,temperature`. 
3. Cross-reference the data and create a JSON Lines file at `/home/user/dataset_summary.jsonl`.
4. Each line in the JSONL file must represent one binary and be a valid JSON object with exactly these keys:
   - `"filename"`: The basename of the binary (e.g., "exp_a.bin")
   - `"experiment_id"`: The ID from the CSV
   - `"temperature"`: The temperature from the CSV
   - `"architecture"`: The extracted machine architecture string (exactly as output by the header parsing tool, trimming leading/trailing whitespace if necessary)
   - `"entry_point"`: The extracted entry point address string

You may use standard Linux utilities available in Bash (like `readelf`, `jq`, `awk`, `grep`, etc.). Please run the necessary commands to generate `/home/user/dataset_summary.jsonl` directly.