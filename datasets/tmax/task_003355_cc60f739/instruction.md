You are helping a technical writer organize their documentation pipeline. You need to build a Go service that acts as an automated documentation publisher.

We have a vendored archive utility package located at `/app/vendored/ziputil`. This package is intended to be used for extracting `.zip` archives. However, it has two problems that you need to fix:
1. Its `go.mod` is incorrectly configured and has a syntax or naming issue preventing it from being imported locally. Fix it so it can be used by your Go service.
2. The `Extract` function in `ziputil.go` is vulnerable to a "Zip Slip" attack (it allows files to be extracted outside the target destination directory if the archive contains paths like `../../file`). You must modify the code to prevent this. Any file that attempts to escape the destination directory must be skipped silently.

Once you have fixed the vendored package, write a Go service in `/home/user/docserver` that does the following:
1. Listens for HTTP requests on `127.0.0.1:8080`.
2. Continuously watches the directory `/home/user/incoming` for new `.zip` files (you can use a simple ticker or file system events).
3. When a new `.zip` file is detected:
   - Extract it into `/home/user/extracted/` using the fixed `ziputil` package.
   - Read the `manifest.json` file from the root of the extracted files. The JSON is an array of objects: `[{"source": "raw/doc1.md", "published_path": "guides/doc1.md", "version": "v2.1"}]`.
   - For each entry in the manifest, perform text transformation on the `source` markdown file: replace all occurrences of the literal string `__VERSION__` with the `version` value from the JSON.
   - Create symbolic links in the directory `/home/user/www/` corresponding to the `published_path` that point to the transformed markdown file in `/home/user/extracted/`. For example, `/home/user/www/guides/doc1.md` should be a symlink to `/home/user/extracted/raw/doc1.md`. Ensure parent directories in `/home/user/www/` are created as needed.
   - Delete the `.zip` file from `/home/user/incoming` after successful processing.
4. Serve the contents of `/home/user/www/` over HTTP at the path `/docs/`. For example, a request to `GET /docs/guides/doc1.md` should serve the linked markdown file.

The system will verify your solution by dropping a malicious `.zip` into `/home/user/incoming/` and then issuing HTTP requests to your server to ensure the files were processed correctly and the Zip Slip vulnerability was mitigated.

Ensure your Go service is compiled, running, and listening on port 8080 when you finish the task. Do not stop the service before completing the task.