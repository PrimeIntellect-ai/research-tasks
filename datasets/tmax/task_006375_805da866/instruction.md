You are an artifact manager maintaining a binary repository. The repository's upload system writes multi-line log records documenting the status of incoming artifacts. 

You have been tasked with generating a master manifest of all currently "VERIFIED" artifacts. 

The logs are located in `/home/user/logs/`. The upload system uses a quirky custom archiving format for transit: every log file in this directory ending in `.b64z` is a standard `gzip` compressed file that has subsequently been `base64` encoded. 

If you decode and decompress them, you will find streams of multi-line records formatted exactly like this:
```
===ARTIFACT===
File: component_v1.tar.gz
Uploader: CI_System
Status: VERIFIED
Timestamp: 1699999999
===END===
```

Your task:
1. Process all `.b64z` files in `/home/user/logs/`.
2. Parse the multi-line records to identify the `File` names of all artifacts that have a `Status: VERIFIED`.
3. Create a consolidated manifest of these verified files.
4. **CRITICAL:** A repository mirroring service constantly reads the manifest file. To prevent it from reading a partially written file, you **must** use an atomic write process. Write your results to a temporary file first, and then atomically move (`mv`) it to the final destination at `/home/user/manifest.txt`.

The final `/home/user/manifest.txt` must contain exactly the filenames of the verified artifacts, one per line, sorted alphabetically. Do not include any other text (e.g., do not include "File: " in the output, just the filename).