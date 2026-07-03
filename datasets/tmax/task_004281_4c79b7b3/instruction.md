You are an artifact manager tasked with curating binary repositories to ensure no malicious archives compromise the build system. Specifically, you need to implement a parser for archive manifests that rejects known vulnerable artifacts and prevents "Zip Slip" directory traversal attacks.

We have a video file located at `/app/revocation_list.mp4`. This video is a short screen recording that displays a list of currently revoked `artifact_id`s. 

Your task is to write a Python script at `/home/user/filter_manifest.py` that strictly conforms to the following behavior:

1. **Input:** The script must accept exactly one command-line argument: the path to a JSON manifest file.
2. **Revocation Check:** The script must read the `artifact_id` from the JSON file. If this ID is present in the video `/app/revocation_list.mp4`, the script must print exactly `STATUS: REVOKED` to standard output and exit immediately. (You will need to analyze the video to extract these IDs).
3. **Zip Slip Prevention:** If the artifact is not revoked, print `STATUS: APPROVED`. Then, iterate through the `files` array in the JSON manifest. You must evaluate each `filename` and reject any path that is malicious. A path is malicious if:
   - It is an absolute path (starts with `/`).
   - It contains a null byte (`\0`).
   - When resolved (collapsing `.` and `..` segments according to POSIX standards), it attempts to traverse outside the root directory of the archive (e.g., `../../etc/passwd`, `data/../../../var`, or simply `..`).
4. **Output:** For every file that is **safe**, print its details on a new line in the exact format: `SAFE: <filename> - <sha256>`. Preserve the original order from the JSON file.

**JSON Manifest Format Example:**
```json
{
  "artifact_id": "PROD-9912",
  "files": [
    {"filename": "bin/run.sh", "size": 1024, "sha256": "abc12345"},
    {"filename": "data/../config/settings.xml", "size": 512, "sha256": "def67890"},
    {"filename": "logs/../../../etc/shadow", "size": 256, "sha256": "badbeef"}
  ]
}
```

Make sure `/home/user/filter_manifest.py` is executable (`chmod +x`). Your script will be tested against a large suite of manifests to ensure strict bug-for-bug equivalence with our internal security oracle.