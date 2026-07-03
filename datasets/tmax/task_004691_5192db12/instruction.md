I am setting up a polyglot build system from scratch and I need a robust bash script to fetch and verify dependencies.

Please write a bash script at `/home/user/fetch_deps.sh` that reads a custom dependency manifest file located at `/home/user/build_manifest.bld`. 

The manifest uses a custom tabular data format. Each line represents a dependency and uses the pipe character `|` as a delimiter:
`[LANGUAGE_ID]|[DEPENDENCY_NAME]|[EXPECTED_SHA256]`

Your script must:
1. Parse the manifest line by line. Ignore empty lines.
2. Download each dependency from a local package server running at `http://127.0.0.1:8080/deps/<DEPENDENCY_NAME>`.
3. The server implements strict rate limiting (max 1 request per second). If you request too fast, it will return an HTTP 429 status code. Your script must detect this (or simply pace its requests to avoid it) and successfully download the file.
4. Calculate the SHA256 checksum of the downloaded file.
5. If the download is successful (HTTP 200) and the checksum matches the expected SHA256, move the file to `/home/user/build_cache/<DEPENDENCY_NAME>` and append the exact string `SUCCESS: <DEPENDENCY_NAME>` to `/home/user/build.log`.
6. If the checksum does not match, discard the file and append `CHECKSUM_FAILED: <DEPENDENCY_NAME>` to `/home/user/build.log`.
7. If the server returns an HTTP 404, append `NOT_FOUND: <DEPENDENCY_NAME>` to `/home/user/build.log`.

Make sure the script is executable (`chmod +x /home/user/fetch_deps.sh`). You must create the `/home/user/build_cache/` directory in your script if it doesn't exist. Ensure your script cleanly finishes processing all items in the manifest. You may test your script against the locally running server on port 8080.