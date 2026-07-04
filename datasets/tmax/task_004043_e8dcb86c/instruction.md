You are an AI assistant helping a storage administrator secure their log processing pipeline. 

Recently, the system has been vulnerable to "zip slip" style path traversal attacks where malicious log entries contain paths that escape the intended storage directories. The senior storage administrator left a voice memo detailing the exact rules for a new log sanitizer tool, but they are currently on leave. 

Here is your task:

1. **Transcribe the Audio Instructions**
   You will find an audio file at `/app/admin_instructions.wav`. Use a transcription tool (like whisper, ffmpeg, or python packages you install) to extract the spoken instructions. This will give you the exact base directory and filtering rules you need to implement.

2. **Implement the Log Sanitizer in C++**
   Write a C++ program that reads a multi-line log format from standard input (`stdin`) and writes the validation results to standard output (`stdout`). 

   The input format consists of multiple records separated by blank lines. Each record looks exactly like this:
   ```
   RECORD START
   User: <username>
   Path: <filepath>
   RECORD END
   ```

   Your C++ program must:
   - Parse these multi-line records.
   - Resolve the `Path` to check for path traversal (handling `.` and `..` components).
   - Apply the rules you transcribed from the audio file (e.g., checking the base directory and any file extension rules).
   - For every record parsed, output a single line to standard output:
     - If the path violates the rules (e.g., escapes the base directory, or violates the extension rule), output: `REJECTED: <original_path>`
     - If the path is safe and valid, output: `ACCEPTED: <resolved_normalized_path>`

3. **Compile the Executable**
   Save your code as `/home/user/sanitizer.cpp` and compile it to `/home/user/sanitizer`. 
   
   Your program must exactly match the expected behavior of the company's reference oracle. An automated system will fuzz your compiled `/home/user/sanitizer` binary with thousands of randomized multi-line log inputs to ensure its output is bit-exact equivalent to the reference implementation.