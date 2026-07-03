You are a Configuration Manager tasked with auditing historical server configuration backups to track down an unauthorized change. 

We have a set of historical configuration files located in `/home/user/configs/`. Due to different legacy backup systems, these files are saved in various character encodings, which are indicated by their file extensions:
- `.utf8` files are encoded in UTF-8.
- `.iso88591` files are encoded in ISO-8859-1.
- `.utf16le` files are encoded in UTF-16LE.

Your task is to write a Go program at `/home/user/tracker.go` that processes these files to find a specific anomaly (changepoint) in our server capacity settings.

Requirements for your Go program:
1. **File Processing**: Read all files in `/home/user/configs/`, sorted chronologically by the date in their filename (format: `config_YYYY-MM-DD.<extension>`).
2. **Encoding Handling**: Correctly decode each file into a standard Go string based on its extension. You may need to initialize a Go module and fetch external text encoding packages.
3. **Regex Extraction**: From each file, extract the `ServerName` and `MaxConnections` values. The lines look like this (case-insensitive keys, arbitrary whitespace before/after the colon):
   `ServerName: <name>`
   `MaxConnections: <number>`
4. **Constraint Validation**: Validate the `ServerName`. A valid server name MUST consist of exactly 3 uppercase ASCII letters followed by exactly 2 digits (e.g., `SRV01`, `APP42`). If a file contains an invalid `ServerName` (or is missing it), you MUST completely ignore that file and skip to the next one, even if its connections are anomalous.
5. **Changepoint Detection**: The baseline for `MaxConnections` is 100. Find the FIRST valid file (chronologically) where `MaxConnections` unexpectedly spikes to a value strictly greater than 1000.
6. **Output**: Once the changepoint is found, write the results to `/home/user/changepoint.json` in the following exact format:
   ```json
   {
     "changepoint_date": "YYYY-MM-DD",
     "anomalous_value": <integer_value>,
     "server_name": "<valid_server_name>"
   }
   ```

Do not output anything else to the JSON file. You have full terminal access to create your Go module, install necessary packages (like `golang.org/x/text`), write the code, and execute it.