You are managing a custom configuration tracker that stores incremental configuration changes in Write-Ahead Log (WAL) formats, securely packaged in nested archives. 

Your task is to reconstruct the final configuration state for a specific service by extracting and parsing these fragmented log files.

The system stores its backups in `/home/user/config_backups/`. 
Inside this directory, there are multiple ZIP archives (`.zip`). 
Inside each ZIP archive, there are several GZIP compressed tarballs (`.tar.gz`). 
Inside these tarballs, there are custom `.wal` files tracking configuration changes for different services.

The `.wal` files contain plain text with the following structure on each line:
`[TIMESTAMP] [SERVICE_NAME] [OPERATION] [KEY] [VALUE]`

Where:
- `TIMESTAMP` is an integer UNIX timestamp.
- `SERVICE_NAME` is the name of the service (e.g., `web_server`, `db_server`).
- `OPERATION` is either `SET` or `DELETE`. If `DELETE`, the `VALUE` column will be empty.
- `KEY` is the configuration parameter name.
- `VALUE` is the configuration parameter value (can be a string, integer, etc. Treat all as strings initially, but preserve exactly what is in the log. `VALUE` might contain spaces, so take everything after the `KEY` as the value).

Example WAL lines:
`1690000001 web_server SET port 8080`
`1690000005 db_server SET max_connections 100`
`1690000010 web_server DELETE host_ip `
`1690000015 web_server SET welcome_message Hello World`

Your goal is to reconstruct the *final* configuration state specifically for the `api_gateway` service.
To do this:
1. Search through all nested archives in `/home/user/config_backups/`.
2. Extract all `.wal` logs.
3. Parse the WAL entries related ONLY to the `api_gateway` service.
4. Apply the operations strictly in ascending order of their `TIMESTAMP` to build the final dictionary of key-value pairs. (If a key is SET, add/update it. If a key is DELETE, remove it if it exists).
5. Write the final state to a JSON file at `/home/user/api_gateway_config.json`. The JSON should be a flat object with the configuration keys and their final string values. Format it with an indentation of 4 spaces.

Requirements:
- Write a Python script to perform this task automatically. 
- You may use standard library modules. 
- Ensure that the final JSON strictly represents the state after processing all logs across all nested archives in chronological order.