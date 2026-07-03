You are tasked with setting up a configuration management tracking service using a locally vendored package called `bash-conf-tracker`. This tool is designed to receive raw server configuration data over HTTP, normalize it, deduplicate entries, validate against a schema, and store the resulting JSON locally.

However, the vendored package currently has some issues and requires your intervention to fix and deploy.

Here are the requirements:
1. **Fix the Vendored Package**: The source code is located at `/app/bash-conf-tracker`. 
   - The package contains a `normalize.sh` script used to parse incoming `KEY=VALUE` payloads. Unfortunately, it has a common bash bug: it drops the last line of the input if it doesn't end with a newline character. You must fix this parsing logic so it processes all lines perfectly.
   - The `Makefile` in the directory has a typo in the `install` target. It tries to copy the scripts to `/user/bin/` instead of `/usr/local/bin/`. Fix the Makefile and run `make install`.
   
2. **Data Processing & Normalization Rules**:
   - The service receives raw text via POST requests.
   - Keys must be lowercased and stripped of surrounding whitespace.
   - Values must be stripped of surrounding whitespace and quotes.
   - If duplicate keys exist in the payload, the *last* defined value should be kept.
   - The payload MUST contain a `hostname` key. If it does not, the ingestion should fail (return HTTP 400).
   
3. **Run the Service**:
   - The package provides a script `start_server.sh <port>` that starts a lightweight `socat`-based HTTP server.
   - You must start this service listening on exactly `127.0.0.1:9090`.
   - The service must accept `POST /upload` with the raw text payload, processing it and saving the normalized JSON to `/home/user/configs/<hostname>.json`.
   - The service must accept `GET /config?host=<hostname>` and return the corresponding JSON file with a `200 OK` status, or `404 Not Found` if the host hasn't reported in.

Please fix the vendored code, install it, ensure the data directory `/home/user/configs/` exists, and start the service in the background so it is ready to receive HTTP requests.