You are a data scientist tasked with building a robust data quality filter for a fleet of remote IoT sensors. 

Your manager has recorded a short voice memo detailing the exact statistical rules and missing-value conditions that define a "corrupted" or "poisoned" dataset. 

Here are your instructions:
1. Locate the audio recording at `/app/guidelines.wav`. You will need to transcribe it (e.g., using a tool like Whisper or standard speech recognition libraries) to understand the strict rejection criteria.
2. The rules described in the audio involve specific missing value checks, outlier detection, and a pipeline requiring bootstrap sampling to estimate statistical thresholds.
3. Write a Python script named `/home/user/filter_dataset.py` that takes a single command-line argument: the path to a CSV file.
    - Example invocation: `python /home/user/filter_dataset.py /path/to/sensor_data.csv`
4. The script must process the CSV and apply the rules exactly as specified in the audio.
5. The script must print exactly `ACCEPT` to standard output if the file passes all data quality checks, or `REJECT` if it violates any of the rules. Do not print anything else to stdout.
6. To help you develop, a few sample datasets might be provided in `/home/user/samples/`, but your script will be evaluated against a hidden adversarial corpus of "clean" and "evil" datasets. 

Ensure your script is reproducible, handles edge cases (like trailing spaces in column names or varying row counts), and strictly sets any random seeds mentioned in the audio memo to ensure reproducible bootstrap estimates.