You are a mobile build engineer maintaining the backend pipelines for our continuous integration system. You need to resolve three pending issues: fixing a broken build tool, creating a sanitizer for build manifests, and setting up a local reverse proxy for artifact caching.

**Part 1: Fix the Vendored Build Tool**
We use a custom Python library backed by a Rust extension to optimize asset packaging. Its source is vendored at `/app/vendored_package/mobile_asset_builder`. 
Currently, it fails to compile because a junior engineer introduced a Rust borrow checker error in `src/lib.rs`.
1. Inspect the Rust source and fix the ownership/borrowing error.
2. Build and install the package globally into your local Python environment using `pip install ./mobile_asset_builder` from within the `/app/vendored_package/` directory.

**Part 2: Manifest Sanitizer**
Mobile clients upload build manifests to the pipeline. We have a set of clean and malicious test manifests located in `/app/corpus/clean` and `/app/corpus/evil`.
Each file contains a JSON object that has been encoded in UTF-16LE and then Base64-encoded. 
Write a Python script at `/home/user/sanitizer.py` that takes a single file path as a command-line argument.
The script must:
1. Read the file, Base64-decode it, and decode the resulting bytes using UTF-16LE to get the JSON string.
2. Parse the JSON.
3. Inspect the `output_dir` string field. If it contains the substring `../` (path traversal attempt), the script must exit with status code `1` (Reject).
4. Otherwise, it must exit with status code `0` (Accept).

**Part 3: Reverse Proxy Configuration**
We need an Nginx configuration file to proxy requests from our build nodes to an internal artifact server.
Create an Nginx config file at `/home/user/proxy.conf` that:
1. Listens on port `8080`.
2. Proxies all requests (`/`) to `http://127.0.0.1:9000`.
3. Adds the HTTP header `X-Mobile-Pipeline: secured` to the proxied request.
Note: Format the config so it is valid Nginx syntax. You do not need to start Nginx, just provide the configuration file.