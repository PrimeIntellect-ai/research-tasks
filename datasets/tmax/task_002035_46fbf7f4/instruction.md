You are tasked with fixing a configuration management ETL pipeline that has been corrupted by a retry bug, leading to duplicate and noisy records. 

First, locate the sysadmin's audio memo at `/app/audio/sysadmin_memo.wav`. You will need to transcribe this audio file (e.g., using a transcription tool or library like `whisper`) to discover the new default "load factor" value spoken by the admin.

Second, write a Python CLI script at `/home/user/process_configs.py` that processes a directory of JSON configuration logs. 
The script must accept two arguments: `--input-dir` and `--output-dir`.

Each JSON file in the input directory contains a list of records with the following schema:
```json
[
  {
    "record_id": "uuid",
    "timestamp": 1690000000.5,
    "metrics": [0.1, 0.5, 0.2, 0.9],
    "load_factor": null
  }
]
```

Your script must perform the following pipeline for each file:
1. **Imputation:** For any record where `load_factor` is `null`, impute it with the exact numerical value spoken in the audio memo.
2. **Filtering (ETL Bug Detection):** Determine if the file is corrupted by the ETL retry bug. A file is considered "corrupted" if it contains ANY two records that satisfy BOTH of these conditions:
   - The absolute difference between their `timestamp` values is `<= 2.0` seconds.
   - The Euclidean distance between their 4-dimensional `metrics` arrays is `< 0.05`.
3. **Output:** 
   - If the file is **corrupted**, REJECT it (do not write it to the output directory).
   - If the file is **clean**, ACCEPT it by writing the fully imputed JSON array to the `--output-dir` using the exact same filename.

Ensure your code is efficient and strictly follows the mathematical definition of Euclidean distance. You may install any necessary dependencies using `pip` or `apt`.