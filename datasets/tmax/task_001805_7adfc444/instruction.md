You are tasked with organizing and refactoring a legacy project's source files. 

The lead developer left a voice memo detailing a specific text-replacement macro that needs to be applied to the codebase, along with specific file-search criteria. This memo is located at `/app/voice_memo.wav`. You will need to extract the instructions from this audio file (you may install and use any transcription tools like `whisper` or Python libraries as needed).

Based on the instructions in the memo, you must build a robust Python CLI tool at `/home/user/project_tool.py`.

Your tool must fulfill the following specifications:
1. **Standard I/O Processing**: When run without special search flags, it should read text from `stdin`, apply the exact multi-step text transformation macro described in the voice memo, and write the result to `stdout`.
2. **File Locking**: Because this tool will be invoked concurrently by a massive parallel refactoring script, it must support a `--lockfile <path>` argument. If provided, your script MUST acquire an exclusive lock on the specified file path using `fcntl.flock(fd, fcntl.LOCK_EX)` before reading `stdin` or processing, and release it before exiting.
3. **Metadata-based Search**: The tool must support a `--search <dir>` flag. When this flag is used, it should recursively search the given directory for all files that have the `.log` extension AND were modified within the last 48 hours. It should print the absolute paths of these files to `stdout`, one per line, sorted alphabetically.

The automated verification suite will test your script's transformation logic for bit-exact equivalence against millions of random inputs, test its file-locking behavior under concurrent load, and test its metadata search on a mocked directory structure.

Focus closely on the precise phrasing of the text-replacement rule in the audio memo, as your script's output must perfectly match the expected output.