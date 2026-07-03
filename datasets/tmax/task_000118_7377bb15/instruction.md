You are tasked with building a secure configuration ingestion pipeline for a fleet manager. Recently, an attacker used a "Zip Slip" vulnerability in our nested archive extraction tool to overwrite critical host files via malicious symlinks and path traversals. 

Your objective is to write a Python command-line utility, `/home/user/secure_extract.py`, that safely extracts configuration archives while strictly rejecting malicious ones. 

Additionally, we intercepted a video of the attacker's terminal (`/app/incident_record.mp4`). To unlock the nested archives, you must analyze this video. Extract the frames using `ffmpeg`. The decryption password for the configuration archives is an integer corresponding to the exact number of frames in the video where the center pixel (x=320, y=240) is pure red `(255, 0, 0)`.

**Requirements for `/home/user/secure_extract.py`:**
1. **Signature:** `python3 secure_extract.py <archive_path> <dest_dir> <password>`
2. **Behavior:**
    * The script must open the provided archive (which may be a `.tar.gz` or `.zip`).
    * Some archives contain nested archives inside them. The script must recursively extract nested archives up to 3 levels deep.
    * If the archive is encrypted, use the password derived from the video.
    * **Sanitization:** The script must analyze all paths, symbolic links, and hard links in the archive. 
    * If any file attempts to extract outside `<dest_dir>` (via absolute paths, `../` traversal, or symlinks pointing outside), the script MUST NOT extract anything, print exactly `REJECT` to stdout, and exit with code `1`.
    * If the archive is safe, it must be fully extracted into `<dest_dir>`, maintaining internal symlink/hardlink structures safely, print exactly `ACCEPT` to stdout, and exit with code `0`.

Ensure your tool correctly handles edge cases like nested symlink loops or hardlinks mimicking path traversals. Output format matters as an automated security scanner will test your script against a large corpus of clean and malicious archives.