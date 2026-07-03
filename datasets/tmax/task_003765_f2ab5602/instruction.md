You are tasked with building a "Configuration Drift Reconstructor" pipeline. A legacy configuration management system has been dumping snapshot data of our server configs over time into a directory, but some data has been lost or corrupted during transit.

Your goal is to build a multi-stage Python pipeline that orchestrates the extraction, validation, imputation, and loading of these configurations.

Here is the setup:
The raw configuration snapshots are located in `/home/user/raw_configs/`. Each file is named in the format `config_<timestamp>.json` (e.g., `config_10.json`).

The expected JSON schema for a configuration file is:
- `max_memory` (integer or null)
- `timeout` (float or null)
- `log_level` (string or null) - restricted to "DEBUG", "INFO", "WARN", "ERROR"
- `feature_flags` (dictionary)

Pipeline Requirements:
1. **Validation Checkpoint (Quality Gate):**
   - Read all files in `/home/user/raw_configs/`.
   - If a file is not valid JSON, it must be moved to `/home/user/quarantine/` and ignored in subsequent steps.
   - Files that are valid JSON but have missing (`null`) values should proceed to the next stage.

2. **Imputation & Interpolation:**
   - Sort the valid configuration files by their timestamp (extracted from the filename).
   - For missing (`null`) **continuous numeric** fields (`max_memory` and `timeout`), perform **linear interpolation** based on the timestamp. For example, if `config_10.json` has `max_memory: 1024` and `config_30.json` has `max_memory: 3072`, then a `null` in `config_20.json` should be imputed as `2048`. (Assume endpoints are never missing). Ensure `max_memory` is output as an integer, and `timeout` as a float.
   - For missing (`null`) **categorical** fields (`log_level`), perform **forward-fill** (use the most recent previous valid value ordered by timestamp). If the very first config is missing a `log_level`, default it to `"INFO"`.

3. **Logging & Monitoring:**
   - Use Python's built-in `logging` module to track the pipeline stages.
   - Write logs to `/home/user/pipeline.log`.
   - The log must include these exact substring formats at minimum:
     - `[STAGE: VALIDATION] Quarantined <N> invalid files.`
     - `[STAGE: IMPUTATION] Imputed <N> missing values across all files.`
     - `[STAGE: LOAD] Successfully wrote <N> reconstructed configs.`

4. **Output/Load:**
   - Write the fully reconstructed, valid JSON configurations to `/home/user/reconstructed_configs/`, preserving the original filenames.

5. **Orchestration:**
   - Write a shell script at `/home/user/run_pipeline.sh` that, when executed, sets up any necessary Python environments/dependencies, runs your Python pipeline script, and exits successfully.

Please create the Python script, the orchestration script, and ensure the pipeline fulfills all requirements.