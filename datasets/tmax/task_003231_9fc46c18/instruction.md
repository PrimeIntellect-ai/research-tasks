We are migrating our legacy configuration management system. As part of this process, we are tracking historical configuration changes stored as massive multi-line log records across our servers. Recently, an attacker attempted to poison our change-tracking repository with malicious configuration entries designed to exploit a vulnerability in our proprietary legacy parser. 

Your task is to build a configuration sanitization script in Python that acts as a pre-filter. 

Here are the details:
1. **The Target System:** We have a stripped proprietary binary located at `/app/legacy_parser`. This tool evaluates multi-line configuration blocks. It usually exits with code `0` for valid configs and `1` for invalid ones. However, it contains a critical flaw: certain combinations of configuration directives cause it to enter a vulnerable state (which you must discover).
2. **The Corpora:** We have prepared two datasets of configuration change records (massive files containing multi-line blocks separated by `---END RECORD---`):
   - `/app/corpora/clean/`: Contains normal, benign configuration updates.
   - `/app/corpora/evil/`: Contains malicious records crafted to trigger the vulnerability in `/app/legacy_parser`.
3. **The Objective:** You must write a Python script at `/home/user/config_filter.py`. Your script will be invoked as:
   `python3 /home/user/config_filter.py <input_dir> <output_dir>`
   - It must iterate through all `.log` files in `<input_dir>` (you must use metadata-based file search to find them, as there are nested subdirectories).
   - Because the log files can be gigabytes in size, you **must** use streaming or memory-mapped I/O (`mmap`) to read them efficiently.
   - It must parse the multi-line records and evaluate them.
   - It must write ONLY the benign records to `<output_dir>`, preserving their exact original formatting and filenames. Records that are malicious (i.e., would trigger the vulnerability in the legacy parser) must be discarded.

To succeed, you will need to analyze the `/app/legacy_parser` binary to understand what constitutes an "evil" record, and then implement a highly efficient parsing and filtering mechanism in Python.