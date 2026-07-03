I am migrating a legacy data processing pipeline from Python 2 to Rust. I need you to translate the core logic, wrap it in a microservice, expose it via a reverse proxy, and prove that the new system produces identical output.

Here is the setup:
1. There is a Python 2 script at `/home/user/legacy_sorter.py`. It reads all CSV files from `/home/user/data/`, merges the records, sorts them descending by the `timestamp` column, and prints a JSON array of the combined records.
2. The current pipeline is slow, so I want to rewrite this logic in Rust.

Your tasks:
1. **Translate & Wrap**: Create a new Rust project at `/home/user/rust_sorter`. Write a Rust HTTP server that listens on `127.0.0.1:3000`. When it receives a `GET /process` request, it must perform the exact same merging and sorting logic on the CSV files in `/home/user/data/` as the Python 2 script. The response body should be the resulting JSON array.
2. **Reverse Proxy Configuration**: We need to put this service behind an Nginx reverse proxy. Create an Nginx configuration file at `/home/user/nginx.conf`. The proxy must listen on `127.0.0.1:8080`, define a `location /` block, and proxy all requests to the Rust server at `127.0.0.1:3000`. Since you do not have root privileges, ensure your `nginx.conf` writes its PID file, access logs, and error logs to `/home/user/` (e.g., `/home/user/nginx.pid`) and disables daemon mode or backgrounding features that require system services.
3. **Run & Verify**: 
   - Compile and start your Rust web service in the background.
   - Start Nginx using your config: `nginx -p /home/user -c /home/user/nginx.conf &`
   - Run the legacy Python 2 script and save its output to `/home/user/py2_output.json`.
   - Send a `GET` request to `http://127.0.0.1:8080/process` and save the response to `/home/user/rust_output.json`.
   - Standardize both JSON files using `jq -c '.'` and save them to `/home/user/py2_min.json` and `/home/user/rust_min.json` respectively.
   - Finally, run `diff -u /home/user/py2_min.json /home/user/rust_min.json > /home/user/diff.txt`.

If the logic is perfectly translated, `/home/user/diff.txt` will be completely empty. Leave the servers running.