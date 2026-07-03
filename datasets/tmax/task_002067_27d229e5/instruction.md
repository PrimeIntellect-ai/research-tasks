You are tasked with building an automated configuration audit pipeline that tracks visual change commits, sanitizes extracted configurations, and generates a structured report. All custom tooling for text processing must be written in C.

Your pipeline must accomplish the following steps:

1. **Video Signal Extraction:** 
   A legacy configuration manager signals a "commit" by flashing a pure white frame on its display output. A capture of this output is located at `/app/config_blinks.mp4` (24 fps). 
   Extract the frame numbers where the video frame is completely white (RGB 255, 255, 255). These frame numbers correspond to the "commit IDs" used in the audit logs.

2. **Adversarial Configuration Sanitizer (C Language):**
   You must write a C program located at `/home/user/config_filter.c` and compile it to `/home/user/config_filter`. 
   - The program must read text from `stdin` and write to `stdout`.
   - It must use regex (e.g., `regex.h`) to detect AWS-style Access Keys. The pattern is the exact string `AKIA` followed immediately by exactly 16 uppercase alphanumeric characters (A-Z, 0-9).
   - When a match is found, the 16 characters following `AKIA` must be replaced with 16 asterisks (`****************`). For example, `AKIA1234567890ABCDEF` becomes `AKIA****************`.
   - Your compiled binary will be strictly tested against an adversarial corpus. It MUST preserve all files in `/app/corpus/clean/` exactly byte-for-byte, and it MUST successfully redact all secrets in `/app/corpus/evil/` without altering surrounding formatting or benign keys.

3. **Log Processing & Sorting:**
   A large system audit log is located at `/app/audit_log.csv`. The format is `commit_id,service_name,config_snippet`.
   - Filter this CSV for rows where the `commit_id` matches the frame numbers you extracted in Step 1.
   - For the matching rows, pass the `config_snippet` field through your `/home/user/config_filter` to redact any secrets.
   - Sort the resulting sanitized records alphabetically by `service_name`.

4. **Template-Based Report Generation:**
   Generate a final Markdown report at `/home/user/final_report.md` with the following exact template structure, populating the parallel processed data:

   ```markdown
   # Configuration Audit Report

   ## Service: [service_name]
   - Commit: [commit_id]
   - Configuration: [sanitized_config_snippet]
   
   ... (repeat for each matched service)
   ```

Ensure all your source code and the final markdown file are properly saved. Your C program must compile without errors using GCC.