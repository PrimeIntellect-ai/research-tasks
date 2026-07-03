You are tasked with restoring a fragmented backup and extracting analytics from a voice log. 

A backup system crashed during an archiving run, leaving behind a directory of un-extensioned blob files in `/app/blobs/` and a CSV manifest file at `/app/backup_manifest.csv`.

The CSV has the following columns: `blob_id, original_path, file_type`. 

Your goal is to write a single Rust program that accomplishes the following:

1. **Backup Restoration via Links:**
   - Parse the `/app/backup_manifest.csv` file.
   - For each entry, recreate the original directory structure under `/app/restored/` and create a **hard link** from the blob file in `/app/blobs/<blob_id>` to `/app/restored/<original_path>`.
   - You must handle missing directories and ensure the links are created successfully.

2. **Audio Processing:**
   - One of the restored files is a system operator's voice log (a standard 16-bit PCM WAV file).
   - Once the hard links are created, your Rust program must locate this `.wav` file in the restored directory tree.
   - Read the audio data and calculate the Root Mean Square (RMS) energy for non-overlapping 100-millisecond windows. 
   - If the final window is less than 100ms, pad the remaining samples with zeros.
   - The RMS for a window of $N$ samples is defined as: $\sqrt{ \frac{1}{N} \sum_{i=1}^{N} x_i^2 }$ (where $x_i$ is the sample value normalized to the range [-1.0, 1.0]).

3. **Atomic Output:**
   - Write the sequence of RMS values as a JSON array of floats (e.g., `[0.012, 0.045, ...]`) to `/app/restored/rms_output.json`.
   - To ensure the backup system isn't left in a corrupted state if the process fails, the write to `rms_output.json` **must be atomic**. You must write to a temporary file first and then rename it to the final destination.

You may use standard Rust crates (e.g., `csv`, `serde`, `serde_json`, `hound`) by initializing a cargo project in `/home/user/restore_tool`. 

The accuracy of your RMS extraction will be verified using a numerical threshold. Your output must have a Mean Squared Error (MSE) of less than 1e-5 compared to the reference data.