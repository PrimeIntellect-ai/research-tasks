You are an AI assistant helping a bioinformatics researcher organize a chaotic stream of continuous sequencing data. 

A previous team member left a data generation script at `/home/user/stream_generator.py`. When executed, this script outputs a massive stream of JSON-formatted sequencing read records to standard output, simulating a live data feed. 

Your task is to write a Python script and a bash pipeline that captures this live stream, organizes the data by experiment, and safely archives it without losing any records.

Here are your exact requirements:

1. **Create the Organizer Script**: Write a Python script at `/home/user/organize_stream.py`. This script must:
   - Read the live JSON lines from standard input (stdin).
   - Parse each JSON object. Every valid object will contain an `experiment_id` key (e.g., "EXP_01", "EXP_02", etc.) and a `sequence_data` key. 
   - Some lines in the stream are corrupted (invalid JSON). Your script must catch these errors and append the raw, exact corrupted string to `/home/user/corrupted_reads.log`.
   - For valid records, append the entire original JSON string to a file specific to that experiment: `/home/user/organized_data/<experiment_id>/reads.jsonl`. You must create the necessary directories on the fly.

2. **Archive Creation**: 
   - Your Python script must detect when the input stream has finished (EOF).
   - Upon EOF, the script must iterate through all the directories in `/home/user/organized_data/` and create a GZIP-compressed tar archive (`.tar.gz`) for each experiment. 
   - The archives must be saved directly in `/home/user/archives/` with the naming convention `<experiment_id>_archive.tar.gz`. The internal structure of the tarball should start with the `reads.jsonl` file (e.g., extracting it should yield `reads.jsonl` or `<experiment_id>/reads.jsonl`, but not absolute paths like `/home/...`).

3. **Execution Pipeline**: 
   - You must execute the stream generator and pipe its output directly into your organizer script. Run: `python3 /home/user/stream_generator.py | python3 /home/user/organize_stream.py`

4. **Verification Log**: 
   - After the pipeline finishes, write a Bash command to list the SHA256 checksums of all `.tar.gz` files in `/home/user/archives/` (sorted alphabetically by filename) and save the output to `/home/user/final_checksums.txt` in the standard `sha256sum` format.

Ensure all file paths are exact as specified. Do not attempt to modify `/home/user/stream_generator.py`.