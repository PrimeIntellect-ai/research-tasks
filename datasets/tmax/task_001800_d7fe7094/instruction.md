You are tasked with building a bash-based ETL pipeline to process and track configuration drift across multiple servers. We receive raw configuration exports in various formats, and we need to normalize them, filter out corrupt exports, and merge them into a single trackable report.

**Background:**
Raw configuration files are dumped into `/home/user/raw_configs/`. Each subdirectory corresponds to a server hostname (e.g., `alpha`, `beta`, `gamma`, `delta`). Inside, there is either a `config.txt` (format: `KEY=VALUE`, one per line) or a `config.json` (a flat JSON object of key-value pairs).

**Your Pipeline Requirements:**

1. **Pipeline DAG Orchestration (`/home/user/pipeline/run.sh`):**
   Create a master script at `/home/user/pipeline/run.sh` that orchestrates the following phases in order. It must be executable.

2. **Phase 1: Validation Checkpoint & Normalization (Parallel Execution):**
   Write a script (or commands within `run.sh`) that processes all servers in `/home/user/raw_configs/` **in parallel** (using `xargs -P`, `wait` with background jobs, or `parallel`).
   - **Quality Gate:** A server's configuration is considered *invalid* and must be completely skipped if any key starts with `ERROR_`.
   - **Normalization:** If a configuration is valid, normalize it to a standard `KEY=VALUE` text format. JSON files must be parsed (using `jq`) into `KEY=VALUE` lines.
   - **Output:** Save the valid, normalized configurations to `/home/user/processed_configs/<server_name>.txt`. Ensure the keys in each file are sorted alphabetically.

3. **Phase 2: Join and Merge (`config_matrix.csv`):**
   After Phase 1 completes, merge all the processed configuration files into a single CSV report located at `/home/user/output/config_matrix.csv`.
   - The CSV must have a header row: `KEY,<server1>,<server2>,...` where the server names are sorted alphabetically.
   - The first column is the configuration `KEY`. Ensure every unique key found across *all valid servers* is represented.
   - The rows must be sorted alphabetically by `KEY`.
   - The subsequent columns must contain the `VALUE` for that key on the corresponding server. If a server does not have that key, leave the cell empty (e.g., `VAL1,,VAL3`).

**Constraints:**
- Use only standard Linux CLI tools (bash, awk, sed, grep, join, sort, jq, xargs). Do not write Python/Perl scripts.
- Ensure all directories exist or are created by your script.
- The final state must be that executing `/home/user/pipeline/run.sh` cleanly creates `/home/user/processed_configs/` and generates the exact correct `/home/user/output/config_matrix.csv`.