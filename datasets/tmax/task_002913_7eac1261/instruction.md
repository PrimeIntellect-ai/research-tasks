I need you to organize a large, messy project directory located at `/app/raw_data/` and compress it efficiently. 

Before processing the files, you must determine the precise magic header length used by this project. To do this, analyze the video file `/app/reference.mp4`. Extract the frames from this video at exactly 1 frame per second. The total number of frames extracted is our magic header length `F`.

Write a Go program located at `/home/user/organize.go` that performs the following tasks:
1. Recursively traverses the `/app/raw_data/` directory.
2. Extracts the first `F` bytes (the binary header) from every file.
3. Computes the full SHA-256 checksum of each file.
4. Uses concurrent workers (goroutines) to process the files. You must use file locking or mutexes to safely coordinate writing results to a single shared manifest file located at `/home/user/manifest.json`. The manifest must be a JSON object mapping the hexadecimal string representation of the `F`-byte header to an array of the absolute file paths that share that header.
5. Generates a heavily deduplicated ZIP archive at `/home/user/organized.zip`. To minimize the file size, if multiple files share the exact same full SHA-256 checksum, your Go program must only include the physical file's contents *once* in the ZIP archive. All subsequent duplicate files must be added to the ZIP archive as symbolic links pointing to the first included file's path.

You may use `ffmpeg` and any standard shell commands to analyze the video and find `F`. The success of your task will be evaluated by the final file size of `/home/user/organized.zip`. A properly deduplicated archive will be significantly smaller than a naive compression.

Run your Go program to generate the manifest and the ZIP archive. Ensure `/home/user/organized.zip` and `/home/user/manifest.json` are present when you finish.