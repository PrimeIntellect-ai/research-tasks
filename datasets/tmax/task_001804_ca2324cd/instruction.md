You are tasked with building a configuration processing pipeline for our fleet management system. We receive incoming configuration state updates from various servers as JSON files. You need to sanitize these incoming payloads, track their configuration drift from a baseline, and aggregate the results. 

Your tasks are:

**1. Fix and Install the Vendored Differ**
We use `dictdiffer` to calculate the exact drift between our baseline and the incoming state. However, the vendored source code at `/app/dictdiffer-0.9.0` contains a deliberate perturbation introduced during a bad refactor.
- Inspect `/app/dictdiffer-0.9.0` to find the issue (it crashes upon import).
- Fix the issue in the source code.
- Install the package locally so it is available to Python 3 in the environment.

**2. Create a Configuration Sanitizer**
Write a Python script at `/home/user/filter.py` that takes a single file path as an argument. The script must parse the JSON configuration update and classify it as "clean" or "evil" based on our strict security policies.

A configuration is "evil" (malicious or invalid) if it violates ANY of these rules:
- Contains the exact substring `/bin/sh` or `bash` anywhere in the `pre_install` or `post_install` hook fields.
- Modifies a file where the `file_path` does not begin with `/etc/app_config/`.
- Contains any environment variables in the `env` dictionary whose key starts with `LD_`.

If the file is "clean", the script must exit with code `0`.
If the file is "evil", the script must exit with code `1`.

We have provided two test corpora for you to evaluate your script during development:
- Clean corpus: `/app/corpora/clean/`
- Evil corpus: `/app/corpora/evil/`
Your script must correctly classify 100% of the files in both corpora.

**3. Build the Data Processing Pipeline**
Write a Bash script at `/home/user/pipeline.sh` that ties this together:
- Iterate through all JSON files in `/app/incoming_configs/`.
- Run `/home/user/filter.py` on each file.
- If the file is "evil", append a log line to `/home/user/pipeline.log` in the format: `[WARN] Rejected <filename>` and skip further processing.
- If the file is "clean", use Python and the fixed `dictdiffer` library to compute the differences between `/app/baseline.json` and the incoming clean config.
- Deduplicate clean configs that belong to the same `server_id` (found in the JSON). If multiple clean configs have the same `server_id`, only process the one with the highest integer `timestamp`.
- For the deduplicated clean configs, log to `/home/user/pipeline.log` in the format: `[INFO] Processed <server_id> with <N> changes` (where `<N>` is the number of top-level diff tuples returned by `dictdiffer`).

All paths must be absolute. Ensure `/home/user/pipeline.sh` is executable.