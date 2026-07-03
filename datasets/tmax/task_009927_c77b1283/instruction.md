You are an AI assistant helping a climate researcher organize a messy dataset of sensor logs. 

The researcher has provided a raw dataset archive at `/home/user/raw_data.tar.gz`. This archive contains a directory called `sensor_logs` with several unorganized log files. Each log file contains multi-line records from various sensors.

The format of each multi-line record is exactly as follows:
```
===BEGIN_RECORD===
Timestamp: YYYY-MM-DDTHH:MM:SSZ
SensorID: <ID>
Status: <OK|ERROR|CALIBRATING>
Reading: <float>
===END_RECORD===
```

Your task is to write and execute a Python script (or use bash commands) to process this dataset according to the following strict pipeline:

1. **Extract**: Extract `/home/user/raw_data.tar.gz` into `/home/user/workspace/`.
2. **Filter & Merge**: Parse all `.log` files in alphabetical order by filename. Extract all complete multi-line records. Discard any records where the `Status` is `ERROR` or `CALIBRATING`. Keep only records where `Status: OK`.
3. **Chunk**: Merge all the valid records in the order they were read, and then split them into chunked files. Each chunked file must contain exactly 10 valid records (the final file may contain fewer if the total is not divisible by 10).
4. **Rename**: Save these chunked files in a new directory `/home/user/processed_data/`. Name each file based on the timestamps of the first and last records within that specific chunk. 
   The naming convention MUST be: `dataset_from_<start>_to_<end>.log`
   Where `<start>` and `<end>` are the timestamps from the chunk, converted to the format `YYYYMMDD_HHMMSS`. 
   (For example: `dataset_from_20231001_081530_to_20231001_092015.log`).
5. **Archive**: Once the processed directory is fully populated, create a zip archive of the `/home/user/processed_data/` directory and save it as `/home/user/clean_dataset.zip`. Ensure the files inside the zip are under the `processed_data/` folder structure, not absolute paths.

Requirements:
- Ensure your script robustly handles the multi-line parsing.
- You must create the final zip file at exactly `/home/user/clean_dataset.zip`.
- Do not modify the original archive.