You are tasked with recovering and serving a set of legacy network configurations for a configuration manager system. The previous system crashed, leaving only a backup archive and a screenshot of the master schema. 

Follow these exact steps to complete the task:

1. **Extract Information from Image:**
   There is an image file located at `/app/legacy_schema.png`. Use `tesseract` to extract the text from this image. The image contains two critical pieces of information: a `MASTER_TOKEN` and a `SERVICE_PORT`. 

2. **Process the Backup Archive:**
   There is a zip archive at `/app/backup_configs.zip` containing old configuration files. 
   - Extract the contents to `/home/user/configs/`.
   - Verify the integrity of the archive. Some files inside might be corrupted; only keep the valid ones.
   - Bulk rename all the valid extracted files from the `.conf.bak` extension to `.json`.

3. **Text Transformation:**
   Inside the valid `.json` files, there is a placeholder string `{{TOKEN_PLACEHOLDER}}`. Use standard Linux text processing tools (like `sed`, `awk`, or `vim` in a script) to replace every instance of `{{TOKEN_PLACEHOLDER}}` with the actual `MASTER_TOKEN` value extracted from the image.

4. **Serve via Rust:**
   Write and execute a Rust HTTP server (using standard libraries or crates like `axum` or `actix-web`) in `/home/user/server/`. 
   - The server must listen on `127.0.0.1` at the exact `SERVICE_PORT` extracted from the image.
   - It must expose an endpoint: `GET /api/config/{filename}`.
   - When requested, this endpoint should read the corresponding `.json` file from `/home/user/configs/` and return its contents with a `200 OK` status and `application/json` content type. If the file is not found, return `404 Not Found`.

Leave the Rust server running in the background so the verification system can query it.