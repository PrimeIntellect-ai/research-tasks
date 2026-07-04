You are assisting a researcher in organizing a messy dataset of sensor recordings and log files. The data is located in `/home/user/dataset/`.

Here is the situation:
1. There is a configuration file at `/home/user/dataset/config.ini` that defines several experiment runs. It maps each `Experiment ID` to a specific log file and a binary data file.
2. The log files are stored in `/home/user/dataset/logs/` and contain multi-line records. Each record block starts with a timestamp like `[YYYY-MM-DD HH:MM:SS]`. 
3. The binary data files are stored in `/home/user/dataset/bin/`.
4. An experiment is considered "successful" ONLY IF its log file contains a multi-line record block where one line is exactly `STATUS: SUCCESS` and the immediately following line is exactly `QUALITY: HIGH`.

Your task is to write and execute a Python script (`/home/user/curate_datasets.py`) that performs the following:
1. Parses `/home/user/dataset/config.ini` to understand the mapping of experiments to their respective files.
2. Reads the log files to determine which experiments were successful based on the multi-line criteria.
3. Creates a compressed gzip tar archive at `/home/user/curated_archive.tar.gz`.
4. Inside the archive, include ONLY the successful experiments. For each successful experiment, create a folder named after the Experiment ID (e.g., `EXP-001/`). Inside that folder, place both its log file and its binary data file.

Constraints:
- You must use Python to perform the parsing and archiving.
- The archive must be a valid `.tar.gz` file.
- Do not include failed experiments in the archive.
- Paths inside the archive should start with the Experiment ID folder (e.g., `EXP-001/exp1.log`), do not include the absolute host path (like `home/user/...`) inside the tar structure.