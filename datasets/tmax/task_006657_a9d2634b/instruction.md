You are acting as a localization engineer. We have a messy JSON file of translations that needs to be normalized, imputed, and processed through a pipeline. 

Your task is to write a Rust program that cleans this data, orchestrate it via a Makefile, and prepare a cron schedule for automated runs.

Here are the requirements:

1. **Rust Program**: Create a Rust project named `loc_tool` in `/home/user/loc_tool`. The program must read an input JSON file and write a processed JSON file. 
   - Accept input and output file paths as command line arguments (e.g., `cargo run -- <input> <output>`).
   - The input is a JSON array of objects. Each object has a `KEY` (or `key`, `Key`, etc. - the casing and whitespace might be inconsistent) and language codes (like `en`, `es`, `fr`).
   - **Normalization**: 
     - Standardize the key name: extract the key, trim leading/trailing whitespace, lowercase it, and replace any internal spaces with underscores. Output this as the `key` field.
     - Standardize placeholders: translations might contain variables formatted as `{{var}}`, `[var]`, or `{var}`. Convert all of them to the `{var}` format.
   - **Imputation**: 
     - If a translation for any language (other than English) is missing, `null`, or an empty string `""`, impute it by falling back to the English (`en`) translation. Every object in the output must have exactly the same language keys as it had in the input, plus the normalized `key`. Do not add language keys that weren't present in that specific object, just fill the missing/empty values for the keys that exist.
   - **Output**: The output must be a valid JSON array of objects, sorted alphabetically by the normalized `key`. Output must be beautifully formatted (pretty printed).

2. **Orchestration**: Create a Makefile at `/home/user/Makefile` with a target named `process`. When we run `make process`, it should compile your Rust project (if needed) and run it to read `/home/user/input.json` and output to `/home/user/output.json`.

3. **Cron Scheduling**: Create a file at `/home/user/cronjob` containing exactly one line with a valid cron expression and command to run the Makefile target `process` in the `/home/user` directory every Tuesday at 3:15 AM. Use `cd /home/user && make process` as the command.

The input file is located at `/home/user/input.json`.