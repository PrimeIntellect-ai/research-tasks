You are a backup administrator tasked with archiving legacy server logs and analyzing a surveillance video of the server room to document a hardware failure incident.

Your workspace is in `/app/`.

1. **Log Parsing and Archival (Go)**
You have a directory `/app/legacy_logs/` containing hundreds of log files. Over the years, these were written in mixed encodings—some are in UTF-16LE and some are in ISO-8859-1.
Write a Go program (save it in `/app/archiver/main.go`) that performs the following:
*   Recursively traverses the `/app/legacy_logs/` directory.
*   Reads each file, determines its character encoding, and converts the text to UTF-8.
*   Extracts only the lines containing the exact string `CRITICAL_BACKUP_FAILURE`.
*   Consolidates all these lines and writes them to `/app/archive_stage/aggregated.log`.
*   **Crucial**: The write must be atomic. Your Go program must write the output to a temporary file first, and only after a successful write, rename it to `/app/archive_stage/aggregated.log`. 

2. **Video Audit**
During the failure, the server rack's emergency light triggered. A video recording is available at `/app/audit.mp4`.
*   Analyze the video (you may use `ffmpeg` to extract frames and write a small script to analyze them).
*   Count the total number of frames where the mean pixel intensity (grayscale average) is greater than 100 (indicating the emergency light was flashing).
*   Write this exact integer count to `/app/archive_stage/light_frames.txt`.

3. **Final Packaging**
*   Ensure the `/app/archive_stage/` directory contains exactly `aggregated.log` and `light_frames.txt`.
*   Create a compressed tarball of this directory at `/app/final_backup.tar.gz`.

Ensure all code dependencies are managed via Go modules (`go mod init` and `go get` as needed). You may use third-party libraries for encoding detection/conversion in Go (e.g., `golang.org/x/text`).