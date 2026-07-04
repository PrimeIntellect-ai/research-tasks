You are tasked with consolidating configuration logs from multiple legacy and modern devices into a single, unified state file. You act as a configuration manager tracking changes across a heterogeneous fleet of devices. 

In `/home/user/config_tracker.ini`, you will find a configuration file that registers several devices. For each device, it specifies:
- `path`: The absolute path to the device's configuration change log.
- `format`: The structured format of the log (`xml`, `csv`, or `json`).
- `encoding`: The character encoding of the log file (e.g., `iso-8859-1`, `utf-16le`, `utf-8`).

Each log contains a history of configuration parameter updates. An update consists of a parameter name, a new value, and an integer timestamp. Because these are change logs, a parameter might be updated multiple times; you only care about the **latest** value for each parameter (the one with the highest timestamp).

Here is how the data is structured in each format:
- **XML**: A root `<log>` element containing multiple `<update>` elements. Each `<update>` has `<param>`, `<value>`, and `<time>` child elements.
- **CSV**: A file with a header row `parameter,value,timestamp`.
- **JSON**: An array of objects, where each object has keys `p` (parameter), `v` (value), and `t` (timestamp).

Your task is to write a script (in the language of your choice) to:
1. Parse `/home/user/config_tracker.ini`.
2. Read and decode each specified log file using the correct character encoding.
3. Parse the specific data formats.
4. Determine the final, most recent value for every parameter on every device based on the timestamps.
5. Write the final consolidated state to `/home/user/final_configs.json`.

The output file `/home/user/final_configs.json` must be a valid, UTF-8 encoded JSON file with the following exact structure:
```json
{
  "device_name": {
    "parameter_name": "final_value"
  }
}
```
The `device_name` keys must match the section headers in the `.ini` file (e.g., `device_alpha`). Ensure all timestamps are treated as integers when finding the maximum.