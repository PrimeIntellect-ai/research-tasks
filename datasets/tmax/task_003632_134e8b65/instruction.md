You are an AI assistant helping a developer organize and parse a messy collection of project logs. The project relies on a hybrid logging format that mixes structured JSON logs and raw GCode machine instructions.

Your task is to write a robust Bash script located at `/home/user/parser.sh` that takes a single file path as its first argument, parses the file line by line, and prints the normalized output to standard output (`stdout`).

**Parsing Rules:**
1. If a line is a valid JSON object (starts with `{` and ends with `}`), extract the value of the `message` field. Output it exactly as: `JSON_MSG: <value>`. If the `message` key does not exist or the line is invalid JSON, output `JSON_MSG: NULL`.
2. If a line represents a GCode command (starts with `G` or `M` followed immediately by numbers, e.g., `G1 X10` or `M104 S200`), extract ONLY the command portion (the `G` or `M` and the numbers, ignoring any parameters like `X10`). Output it exactly as: `GCODE: <command>`.
3. If a line does not match the above two criteria, it is considered plain text. Output it exactly as: `TEXT: <uppercased_line>` (convert the entire line to uppercase).
4. **Exceptions & Overrides:** The lead developer left an audio memo at `/app/project_memo.wav` detailing a critical, late-breaking rule regarding how specific commands or messages should be handled or skipped. You must transcribe and understand this audio file to implement the final parsing logic correctly.

**Requirements:**
- Your script must be written entirely in Bash (you may use standard CLI tools like `jq`, `grep`, `sed`, `awk`, `tr`, etc., available on standard Linux environments).
- Make sure your script is executable (`chmod +x /home/user/parser.sh`).
- Your script will be aggressively tested against thousands of randomly generated log files. Its output must exactly match the behavior of a hidden reference parser byte-for-byte.

Begin by analyzing the audio file to get the complete parsing requirements, then write your script at `/home/user/parser.sh`.