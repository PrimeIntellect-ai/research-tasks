You are an IT support technician responding to an escalated ticket (Ticket #8831). 

**Ticket Details:**
"Hi Support, we have a legacy C++ data extraction tool located at `/app/legacy_decoder`. It parses our proprietary `.dat` telemetry logs into JSON lines. Unfortunately, it only runs on our old architecture, and the original developer left without leaving the source code. The binary is stripped.
We started migrating this to Python in `/home/user/pipeline_repo`, but the script is incomplete and fails to decode certain encrypted fields correctly because we lost the decryption key (though I think the dev accidentally committed it to the repo once before removing it).

**Your Objectives:**
1. **Forensics & RE**: Reverse engineer the behavior of `/app/legacy_decoder`. Understand how it reads binary `.dat` files and outputs JSONL. Check the git history in `/home/user/pipeline_repo` to recover the lost decryption key.
2. **Implementation**: Write a pure Python script at `/home/user/pipeline_repo/decoder.py` that replicates the binary's behavior perfectly. It must accept two command-line arguments: an input `.dat` file path and an output `.jsonl` file path.
   Usage: `python3 /home/user/pipeline_repo/decoder.py <input.dat> <output.jsonl>`
3. **Edge Case Handling**: Ensure your Python script properly handles all data types present in the binary's output, including EOF markers or malformed length edge-cases that the binary gracefully skips.
4. **Regression Test**: Write a script `/home/user/pipeline_repo/test_regression.py` that generates a variety of test `.dat` files, runs both the binary and your Python script on them, and ensures the outputs are strictly identical.

Once you have perfected `/home/user/pipeline_repo/decoder.py`, the automated grading system will run it against a massive, hidden dataset `/app/hidden_test.dat` and evaluate the output's accuracy. Ensure your script is efficient and perfectly matches the binary's logic.