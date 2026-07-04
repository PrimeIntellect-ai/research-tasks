You are debugging a failing build pipeline in `/home/user/project`. The build relies on a Python script, `parse_config.py`, which recently crashed processing a configuration file. 

Unfortunately, the input file that caused the crash was deleted by the build system's cleanup step, but it was `git add`ed (staged) right before being deleted, though never committed. A log of the crash is preserved in `/home/user/project/build.log`.

Perform the following steps to fix the pipeline:
1. **Recover the deleted file**: Inspect the git repository's dangling objects to find the deleted configuration file. Save the recovered content exactly as it was to `/home/user/project/recovered.json`.
2. **Diagnose and Fix**: Analyze `build.log` to understand the crash. The script is failing because of corrupted input (a specific field is the wrong type). Modify `/home/user/project/parse_config.py` so that:
   - If the `"weight"` field in any JSON object is a string, missing, or invalid, it gracefully defaults to `0` instead of crashing.
   - If the entire file is invalid JSON (e.g., completely random bytes), the script should catch the `json.decoder.JSONDecodeError`, print "Invalid JSON", and exit gracefully with a standard `0` exit code.
3. **Fuzz Testing**: Write a bash script at `/home/user/project/fuzz.sh` that loops 10 times. In each iteration, it should generate a random 50-byte payload from `/dev/urandom`, write it to `test.json`, and run `python3 parse_config.py test.json`. The script must exit with code 0 on all 10 iterations despite the garbage input. 
   
Run your fuzzer once. If successful, write the word `SUCCESS` to `/home/user/project/fuzz_result.txt`.