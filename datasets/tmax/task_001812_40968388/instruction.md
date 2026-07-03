You are tasked with building a Configuration Tracking service that acts as a central hub for applying and verifying configuration changes across our infrastructure. 

First, initialize the base configuration state by parsing a multi-line log file located at `/home/user/base_config.log`. This log contains entries like `[TIMESTAMP] CONFIG_ADD <KEY> <VALUE>`. Extract all the final key-value pairs to build your initial state.

Second, we have a legacy proprietary utility located at `/app/cfg_checksum`. This binary is stripped and possibly packed. It is used to compute a proprietary 32-bit checksum for configuration text. You must figure out how to use this binary (or reverse engineer its algorithm) to calculate checksums for raw configuration data.

Third, write a Python HTTP server that listens on `127.0.0.1:8000`. The server must implement the following specification:
1. Accept `POST` requests on the endpoint `/api/v1/config/push`.
2. Require the HTTP header: `Authorization: Bearer track-configs-2024`.
3. The request body will be a custom binary format representing the configuration patch:
   - Bytes 0-3: Magic bytes `CFG\x01`
   - Bytes 4-7: Uncompressed length of the payload (32-bit unsigned integer, big-endian)
   - Bytes 8-11: Proprietary checksum of the *uncompressed* text payload (32-bit unsigned integer, big-endian)
   - Bytes 12+: zlib-compressed text data containing new configuration lines in the format `KEY=VALUE\n`.
4. Your server must:
   - Decompress the payload.
   - Verify the uncompressed text against the checksum provided in the header using the logic from `/app/cfg_checksum`. If the checksum fails, return HTTP 400.
   - Parse the `KEY=VALUE` lines and update your internal configuration state.
   - Write/overwrite each updated key to the filesystem at `/home/user/config_store/<KEY>.conf` (where the file content is exactly the `<VALUE>`). Create the directory if it doesn't exist.
   - Return an HTTP 200 JSON response: `{"status": "applied", "updated_keys": ["<KEY1>", "<KEY2>"]}`.

Start the Python service in the background and leave it running so our automated verifier can send configuration payloads to it.