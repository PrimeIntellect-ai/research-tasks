You are a script developer responsible for building a CI/CD security gate utility. Your team manages a web application where URL routing rules are updated frequently via patch files. Recently, malicious actors have attempted to inject x86 shellcode into URL parameters, and developers sometimes commit routes with invalid checksums.

Your task is to write a Python utility at `/home/user/scan_patches.py` that classifies a directory of patch files as either "clean" or "evil". 

**Context & Requirements:**
1. **The Video Artifact:** You are provided a video at `/app/salt_video.mp4`. This video is a 4-second, 1 fps recording (4 frames total). Each frame displays a single large, black alphanumeric character on a white background. Read these characters in order to form a 4-character secret string (the "Salt"). You may use `ffmpeg` and `tesseract` to extract this.
2. **Patch Processing:** The input will be a directory containing `.patch` files modifying a file named `routes.conf`. Your script must parse these diffs to find newly added routes (lines starting with `+ROUTE`).
3. **URL Routing & Checksum:** Each added route has the format:
   `+ROUTE <url_path_with_params> CHECKSUM=<md5_hex>`
   A route is considered **valid (clean)** if:
   a) The `<md5_hex>` exactly matches the MD5 hash of the string `<url_path_with_params><Salt>`.
   b) The URL parameters DO NOT contain URL-encoded x86 assembly NOP sleds. Specifically, if any parameter contains the sequence `%90%90%90` (case-insensitive), it is **evil**.
4. **Classification:** A `.patch` file is "evil" if it adds ANY route that fails the checksum OR contains the malicious assembly sequence. If all added routes are valid, or if the patch doesn't add any new routes, it is "clean".

**CLI Interface:**
Your script must be callable exactly as follows:
`python3 /home/user/scan_patches.py --corpus <directory_path> --video /app/salt_video.mp4 --out <output_json_path>`

**Output Format:**
The output must be a valid JSON file mapping the base filename of each patch in the corpus to its classification ("clean" or "evil").
Example:
```json
{
  "update_1.patch": "clean",
  "malicious_update.patch": "evil"
}
```

Write the utility to perfectly separate the two provided test corpora located at `/app/corpus/clean/` and `/app/corpus/evil/`. You have standard Linux tools, `ffmpeg`, `tesseract-ocr`, and Python 3 available.