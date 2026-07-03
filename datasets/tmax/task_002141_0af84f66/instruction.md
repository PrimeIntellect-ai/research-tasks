You are a web developer building a backend feature for a collaborative video editing platform. Users can submit transcript edits as unified diff `.patch` files. You need to build a high-performance filtering system to reject malicious patches, as well as a utility to extract a specific video thumbnail.

Your task is to build a Go command-line tool `videdit` in `/home/user/videdit/` that combines Go concurrency, C shared libraries, and shell integration.

### Part 1: C Shared Library for Patch Validation
For performance and legacy reasons, the patch validation logic must be written in C.
Create a C file `validator.c` and compile it into a shared library `libvalidator.so`.
It must implement the following ABI:
`int validate_patch(const char* filepath);`

The function must read the specified unified diff (`.patch`) file and return `1` if it is CLEAN, and `0` if it is EVIL.
A patch is considered EVIL if any of its added or removed lines (lines starting with exactly a single `+` or `-`, excluding the file header lines `+++` and `---`) contain the substring `[RESTRICTED]` or `[METADATA]`. Otherwise, it is CLEAN.

### Part 2: Go Concurrent Processor
Create a Go program `main.go` that builds into an executable named `videdit`.
It must use `cgo` to link against `libvalidator.so`.
The tool must support the `check` subcommand:
`/home/user/videdit/videdit check <directory>`
This command must:
1. Find all `.patch` files in the given `<directory>`.
2. Process them concurrently using goroutines (do not process them sequentially).
3. Output the result to stdout in the exact format: `<filename>: CLEAN` or `<filename>: EVIL` (one per line).

### Part 3: Video Thumbnail Extractor
The tool must also support a `thumb` subcommand:
`/home/user/videdit/videdit thumb <video_file>`
This command must:
1. Invoke `ffmpeg` to extract exactly one frame from the video at timestamp `00:00:05` (5 seconds).
2. Save it as `thumb.jpg` in the current working directory.
3. Print the text `Thumbnail extracted` to stdout.

### Setup and Constraints
- Put all your code in `/home/user/videdit/`.
- Make sure `libvalidator.so` is accessible at runtime (e.g., set `LD_LIBRARY_PATH` or use rpath).
- You are free to test your implementation against the sample video at `/app/video.mp4` and the sample patches provided in `/app/corpus/clean/` and `/app/corpus/evil/`.