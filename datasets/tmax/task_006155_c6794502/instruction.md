You are an IT support technician responding to an escalated ticket. A user reported that their daily data processing script, `/home/user/process_data.sh`, fails intermittently. Sometimes it works perfectly, but today it is crashing and failing to produce its final output.

The script scans a directory (`/home/user/data/`), calculates the average file size in Megabytes, and attempts to write a summary to a JSON file (`/home/user/output.json`) using `jq`. 

Your task:
1. Diagnose and fix the root causes of the script's failure. There are at least two distinct bugs related to data formatting and encoding.
2. Modify `/home/user/process_data.sh` so that it successfully runs and generates valid JSON in `/home/user/output.json`.
3. The JSON must contain the key `"average_size_mb"` formatted as a valid JSON number (it must have a leading zero if the value is less than 1, to comply with strict JSON standards).
4. The JSON must contain the key `"processed_files"` as an array of strings representing the filenames. 
5. Ensure all files in `/home/user/data/` are processed. One or more files currently in the directory may have non-UTF-8 characters in their filenames. Your script must output valid UTF-8 JSON; any non-UTF-8 filenames should be interpreted as ISO-8859-1 (Latin-1) and correctly converted to UTF-8 for the JSON output. (Do not rename the actual files on disk).

The final script should execute without errors when run as `./process_data.sh` and correctly create `/home/user/output.json`.