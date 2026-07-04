You are a build engineer responsible for validating a recent artifact metadata schema migration. A migration script recently processed a batch of artifact metadata files from schema version 1 to version 2, but we suspect it introduced some errors. 

Your task is to write a Python test script at `/home/user/verify_migration.py` that orchestrates an end-to-end validation of the migration. 

Here are the requirements:
1. **Parse the Migration Log**: The migration logged its output to `/home/user/migration.log`. You must parse this log using a state machine approach to identify which artifacts were marked as successfully migrated. 
   - A migration process for an artifact begins with `[INFO] START migrate <artifact_id>`.
   - It ends with either `[INFO] SUCCESS <artifact_id>` or `[ERROR] FAIL <artifact_id>`.
   - The log is sequential but may contain other noise. You should only validate artifacts that successfully completed their migration according to the log.

2. **Validate Migrated Artifacts**: For every successfully migrated artifact, load its corresponding v1 file from `/home/user/artifacts/v1/<artifact_id>.json` and its v2 file from `/home/user/artifacts/v2/<artifact_id>.json`.
   A valid v2 artifact must satisfy **all** the following conditions:
   - The JSON object must contain a `"version"` key with the integer value `2`.
   - The JSON object must contain an `"id"` key that exactly matches the `"id"` from the v1 file.
   - The JSON object must contain a `"checksum"` key. The value of this key must be the MD5 hash of the **raw file contents** of the corresponding v1 JSON file (the exact bytes of the v1 file).

3. **Generate a Test Report**: Your script must run the validations and write a report to `/home/user/test_report.txt`. 
   - The file should contain the `<artifact_id>` of any artifact that *failed* the validation, one per line, sorted alphabetically.
   - If all successfully migrated artifacts pass validation, the file should contain exactly the text `ALL PASS`.

You do not need to fix the artifacts; just write the test script, execute it, and produce the `test_report.txt`.