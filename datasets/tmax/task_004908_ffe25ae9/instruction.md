You are an automation specialist tasked with building a high-performance JSON-lines validation filter in C. 

We process thousands of log files daily, and we need a tool to sanitise them. Our upstream systems sometimes generate malformed unicode escape sequences, and we also have a dynamically changing operational constraint.

Your tasks:
1. **Extract the Operational Constraint:** We have received an audio memo at `/app/directive.wav`. Transcribe this audio file to discover the secret constraint rule (it dictates a specific value in a specific JSON field that must be rejected).
2. **Build the Sanitiser (C):** Write a C program at `/home/user/sanitiser.c` and compile it to `/home/user/sanitiser`. 
   The program must accept two arguments: an input JSONL file path and an output JSONL file path.
   Usage: `./sanitiser <input.jsonl> <output.jsonl>`
   
   It must read the input line-by-line, and apply the following constraints:
   - **Validation 1 (Unicode):** Reject any line that contains an invalid JSON unicode escape sequence (i.e., `\u` followed by anything other than 4 hexadecimal digits).
   - **Validation 2 (Operational):** Reject any line that violates the rule extracted from `/app/directive.wav`.
   
   Valid lines must be written to the output file exactly as they appeared. Rejected lines must be discarded from the output file, and their line numbers (1-indexed) must be logged to a file named `/home/user/dropped.log` (one number per line).

3. **Performance (Parallelism):** You must process the lines in parallel (e.g., using OpenMP or pthreads) to ensure high throughput, while maintaining the correct output constraint checks.

To pass this task, your compiled `sanitiser` must perfectly preserve safe records and perfectly drop invalid records.