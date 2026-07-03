You are tasked with building an automated configuration management pipeline that processes voice dictations from system administrators, extracts network rules, resolves conflicts, and outputs the final system state.

We have received a voice recording of a sysadmin dictating a series of firewall rule changes in `/app/config_dictation.wav`.

Your objectives are:
1. **Transcribe the Audio**: Use a transcription tool of your choice (e.g., installing `openai-whisper` via pip) to transcribe `/app/config_dictation.wav` to text. The dictation contains sequential commands like "Add rule for IP 192.168.1.50 on port 80", "Remove rule for IP 10.0.0.5 on port 443", etc.
2. **Implement an ETL Processor in C**: Write a C program at `/home/user/config_mgr.c` that reads the transcribed text file.
3. **Structured Extraction**: The C program must use POSIX regex (`<regex.h>`) to parse the text and extract the Action (Add/Remove), IP address, and Port number from each line or sentence. 
4. **Parallel Processing**: Implement multi-threading (`pthreads`) in your C program to process chunks of the transcript in parallel.
5. **Hash-based Deduplication/State Resolution**: The rules are sequential but might contain conflicts (e.g., adding an IP/port, then removing it later, or adding it twice). Implement a hash table in C to resolve the final active state. A "Remove" action should delete the entry if it exists. An "Add" action should insert or update it.
6. **Output**: The C program should output the final active rules to `/home/user/active_config.csv` in the format `IP,Port` (one per line, sorted alphabetically by IP, then numerically by Port).

Compile your C program, run it against your transcript, and ensure `/home/user/active_config.csv` is generated correctly. 

Your final output will be graded based on the Jaccard similarity (Intersection over Union) of the rules in your CSV compared to the ground truth. You must achieve a similarity score of >= 0.90.