You are assisting a technical writer in recovering and organizing an old documentation repository. 

You have been provided with two key artefacts:
1. A custom binary documentation archive at `/home/user/docs.pkg`.
2. An audio dictation file containing missing documentation notes at `/app/doc_notes.wav`.

**Step 1: Fix the Extraction Tool**
The previous writer created a custom archive extractor in C, located at `/home/user/extractor.c`. It uses memory-mapped I/O for fast extraction. However, it contains a critical "zip slip" vulnerability: it blindly trusts file paths in the archive, which can lead to overwriting system files outside the target directory.
- Modify `/home/user/extractor.c` to prevent directory traversal. Specifically, your fix must cause the program to completely **skip** extracting any file whose stored path starts with `/` or contains `../`.
- Compile your fixed program: `gcc -O2 /home/user/extractor.c -o /home/user/extractor`
- Run your compiled extractor on `/home/user/docs.pkg`, extracting its contents into the directory `/home/user/extracted/` (create this directory first). 

**Step 2: Transcribe and Format the Audio Dictation**
The technical writer left an audio dictation in `/app/doc_notes.wav`. 
- Transcribe the English audio using any available tool (e.g., installing `whisper-cpp` or using standard speech-to-text utilities you can install).
- Normalize the transcribed text: convert it entirely to lowercase and remove all punctuation (commas, periods, etc.), leaving only single spaces between words.

**Step 3: Document Assembly**
One of the safely extracted files will be `draft.txt`. It contains a placeholder string `[DICTATION_INSERT]`.
- Use text transformation tools (`sed`, `awk`, or `vim`) to replace the `[DICTATION_INSERT]` placeholder in `draft.txt` with your normalized transcription.
- Save the final assembled document to `/home/user/final_doc.txt`.

Ensure your C code safely handles the memory-mapped boundary conditions and skips malicious paths without crashing.