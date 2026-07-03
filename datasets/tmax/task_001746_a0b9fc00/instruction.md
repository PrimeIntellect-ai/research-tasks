You are an infrastructure engineer automating the provisioning pipeline for our edge network. We use a Git-based workflow to manage configuration scripts, but we need to ensure that no unauthorized routing configurations are pushed to production.

Your tasks are as follows:

1. **Policy Extraction**: 
   There is a screenshot of our security policy located at `/app/network_policy.png`. Use OCR (e.g., `tesseract`) to read the text from this image. It contains the definition of a "blocked" subnet or keyword that must never appear in our provisioning scripts.

2. **Detector Script**:
   Write a Python script at `/home/user/validate_config.py` that acts as a configuration validator.
   - The script must take a single command-line argument: the absolute path to a file.
   - It must read the file and check if it contains any references to the blocked subnet/policy found in the image.
   - If the file is clean, the script MUST exit with status code `0`.
   - If the file is "evil" (violates the policy), the script MUST exit with status code `1`.
   
   To help you develop this, we have provided two directories containing test provisioning scripts:
   - `/app/clean/`: Contains scripts that comply with the policy.
   - `/app/evil/`: Contains scripts that violate the policy.
   Your script must perfectly separate these two corpora.

3. **Git Hook Configuration**:
   - Create a bare Git repository at `/home/user/provisioning.git`.
   - Create a `pre-receive` hook in this repository that would theoretically run your `validate_config.py` script on incoming changes. (For the scope of this task, simply creating the executable bash hook script at `/home/user/provisioning.git/hooks/pre-receive` that exports an environment variable `STRICT_MODE=1` and calls your python script is sufficient).

Ensure your Python script is robust, executable, and handles standard file reading safely. Our automated verifier will strictly test `/home/user/validate_config.py` against a hidden evaluation corpus.