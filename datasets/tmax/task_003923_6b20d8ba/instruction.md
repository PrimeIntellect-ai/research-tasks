I need you to help me organize some scattered project logs. We had a log rotation script that was racing with the writing process, so our logs are currently fragmented across multiple rotated files and subdirectories. 

Here is what you need to do:

1. Look at the configuration file located at `/home/user/organizer_config.json`. It contains a JSON object specifying an `output_dir` and a `component_formats` mapping (which maps component names to desired output file formats: either `csv` or `json`).
2. Search through `/home/user/project_logs` and all its subdirectories for any files starting with `app` and containing `.log` (e.g., `app.log`, `app.log.1`, `app_error.log`).
3. Parse the log lines from all these files. The logs are in this format:
   `[YYYY-MM-DD HH:MM:SS] [LEVEL] [COMPONENT] Message text here`
   *Note: Due to the race condition, some files might contain empty lines or malformed lines that do not start with a `[` timestamp. Ignore any invalid or empty lines.*
4. For each component defined in the `component_formats` mapping of the config file, aggregate its logs across all the files you found.
5. Sort the aggregated logs for each component strictly in chronological order based on the timestamp.
6. Create the `output_dir` specified in the config if it doesn't exist.
7. Save the sorted logs for each component into the `output_dir` using the requested format. Name the files exactly as `<COMPONENT_NAME>_logs.<format>` (all lowercase for the filename).
   - For `csv`: Include a header row `timestamp,level,message`. Quote the message field if necessary.
   - For `json`: Output a JSON array of objects with keys `"timestamp"`, `"level"`, and `"message"`.

Use Python to write a script that performs this consolidation and format conversion. Execute it to generate the final files.