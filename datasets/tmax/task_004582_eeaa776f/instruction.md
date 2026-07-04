You are managing a legacy configuration tracking system that records system state changes in a custom Write-Ahead Log (WAL) format. Currently, a legacy binary (`/app/legacy_tracker`) is used to process these `.wal` files. It traverses a directory of logs, parses the custom WAL format, extracts the configuration chunks, bulk-renames them according to a schema defined in the logs, and merges them to output a final directory state representing the latest configuration.

Unfortunately, `/app/legacy_tracker` is single-threaded and notoriously slow on large datasets due to an inefficient O(N^2) internal merging algorithm.

Your task is to write a highly optimized Rust program that performs the exact same function but is significantly faster. 

**Requirements:**
1. **Analyze the Legacy Binary**: `/app/legacy_tracker` is a stripped ELF binary. You can run it on a small sample directory `/home/user/sample_wals/` to observe its input/output behavior and reverse-engineer the `.wal` format. It takes two arguments: the input WAL directory and the output state directory (e.g., `/app/legacy_tracker /home/user/sample_wals /home/user/sample_out`).
2. **Implement in Rust**: Create a Rust project at `/home/user/fast_tracker`. Your Rust program must accept the same arguments: `cargo run --release -- <input_dir> <output_dir>`.
3. **Parse and Extract**: Your program must traverse the input directory, parse all `.wal` files, and extract the embedded file chunks.
4. **Bulk Rename & Merge**: Resolve the sequence of operations (e.g., creations, updates, deletions) chronologically across all WAL files. Keep only the latest version of each tracked configuration file and write the final merged state to the specified output directory.
5. **Format Conversion**: Any extracted file with a `.gcode_b` extension in the WAL must be converted to plain text GCode during extraction (the legacy binary does this automatically; you must figure out the binary encoding it uses).

**Evaluation:**
Your tool will be evaluated on a massive dataset located at `/home/user/large_wals/`. You must output the exact same final directory structure and file contents as `/app/legacy_tracker`, but your Rust implementation must achieve a significant speedup. Write your output for the large dataset to `/home/user/final_state/`.