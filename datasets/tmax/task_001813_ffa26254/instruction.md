You are assisting a technical writer in organizing and sanitizing a large documentation repository. Recent draft documents have accidentally included sensitive internal project codes, and you need to build an automated pipeline to filter them out before publication.

First, the lead technical writer has left a voice memo detailing the exact format of the leaked sensitive project codes. You will find this audio file at `/app/voice_memo.wav`. Transcribe or listen to this audio (e.g., using `whisper` or other available transcription tools) to understand the exact pattern of the sensitive data that must be redacted.

Next, you must create a sanitization filter. Write an executable script at `/home/user/doc_filter.sh` (or `.py`, as long as it is executable and works as a standard CLI tool). 
Your script must accept a single file path as its first argument. 
- If the file is "clean" (does not contain the sensitive pattern described in the audio), the script must exit with status code `0`.
- If the file is "evil" (contains the sensitive pattern), the script must exit with status code `1`.

We will rigorously verify your filter. Behind the scenes, an automated verifier will test `/home/user/doc_filter.sh` against a hidden adversarial corpus consisting of hundreds of edge-case documents. It must correctly classify 100% of them.

Finally, the technical writer needs you to process the current drafts. 
1. Recursively search `/home/user/drafts/` for all `.md` files modified within the last 7 days.
2. Run your filter on each file.
3. For every "clean" file, append its contents to a master file at `/home/user/compiled_docs.md`.
4. **Crucial Requirement:** Because this compiling process is designed to be run concurrently by multiple technical writers in the future, your command or script that writes to `/home/user/compiled_docs.md` MUST use file locking (e.g., using `flock`) to prevent race conditions during the append operation. 

Ensure `/home/user/doc_filter.sh` is ready and `/home/user/compiled_docs.md` is successfully built.