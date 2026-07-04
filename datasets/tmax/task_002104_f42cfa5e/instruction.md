You are tasked with building a configuration validation filter for our system's configuration manager. We track server resource configuration changes over time, but we suspect some malformed or malicious configurations are being submitted.

First, you need to read the validation policy. Due to a legacy system quirk, the current policy rules are stored as an image at `/app/policy_rules.png`. You will need to use OCR (e.g., `tesseract`, which is preinstalled) to extract the text from this image.

The image defines three critical parameters:
1.  **Imputation Default**: The default memory value (in MB) to use if the `memory` field is missing in a configuration state.
2.  **Max CPU Threshold**: The maximum allowable CPU cores for any single state.
3.  **Max Aggregated Delta**: The maximum allowable absolute sum of changes (deltas) in memory across the entire time-series of a single configuration sequence.

We have a dataset of configuration sequences. Each file is a JSON array of configuration states ordered by time. Each state is a dictionary that may contain `cpu` and `memory` fields. 

Your task is to write a Python script at `/home/user/validate_configs.py` that:
1. Accepts a directory path as a command-line argument.
2. Iterates through all `.json` files in that directory.
3. For each file, extracts the sequence of states.
4. Imputes any missing `memory` values using the rule from the image.
5. Calculates the summary statistics: the absolute sum of day-to-day changes in the `memory` field (i.e., `sum(abs(memory[i] - memory[i-1]))`).
6. Classifies the sequence as INVALID (reject) if:
   - Any single state exceeds the Max CPU Threshold.
   - The total aggregated memory delta exceeds the Max Aggregated Delta.
   - The sequence has more than 2 missing fields overall (cpu and memory combined) before imputation.
7. Otherwise, the sequence is VALID (accept).

Your script must print the filename and its validation result to standard output in the format: `[filename]: VALID` or `[filename]: INVALID`.

Ensure your script is perfectly accurate based on the policy rules hidden in `/app/policy_rules.png`.