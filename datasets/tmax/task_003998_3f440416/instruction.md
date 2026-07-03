You are acting as a release manager preparing a new deployment. You need to automate the parsing, merging, and serving of release manifests. Complete the following multi-stage workflow:

1. **Extract Release Token:**
   There is an image file located at `/app/release_token.png` which contains a secret release token printed as text. Use OCR (e.g., `tesseract`) to extract this token. Note this token for later use.

2. **Merge and Sort Manifests:**
   The directory `/app/manifests/` contains multiple CSV files (`part1.csv`, `part2.csv`, `part3.csv`). Each file contains a list of deployment artifacts with columns: `ArtifactID,Name,Version`. 
   Merge all these CSV files into a single file `/app/merged_manifest.csv`, sorted alphabetically by `ArtifactID`. Ensure the header row `ArtifactID,Name,Version` appears exactly once at the top of the merged file.

3. **Apply Updates:**
   You have been provided with a patch file `/app/updates.patch`. Apply this patch to `/app/merged_manifest.csv` to update specific artifact versions. Save the successfully patched file as `/app/final_manifest.csv`.

4. **Fix Memory Issue in Processing Script:**
   The script `/app/process_logs.sh` is supposed to parse a large log file `/app/release.log` to extract unique error codes, but it currently crashes or hangs due to inefficient memory usage (it tries to load everything into a bash array). Refactor the bash script to be memory efficient using standard stream-processing tools (like `awk`, `sort`, `uniq`). Run your fixed script to process `/app/release.log` and output the result to `/app/processed_logs.txt`.

5. **Serve the Release Manifest:**
   Write a Bash script `/app/server.sh` that brings up an HTTP service listening on `127.0.0.1:8080` (you may use `nc`, `socat`, or similar tools). 
   The server must handle `GET /manifest` requests. 
   - If the request includes the HTTP header `Authorization: Bearer <TOKEN>` (where `<TOKEN>` is the exact token extracted from the image in step 1), the server must respond with a `200 OK` status and the contents of `/app/final_manifest.csv` as the body.
   - If the header is missing or incorrect, it must respond with a `401 Unauthorized` status.
   Leave this server running in the background.

Ensure all output files are placed at the exact paths specified.