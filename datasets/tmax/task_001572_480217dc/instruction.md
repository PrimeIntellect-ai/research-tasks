You are an SRE forensics investigator tasked with fixing an uptime monitoring pipeline. Recently, our monitoring shell scripts have been crashing, and false "100% uptime" metrics are being reported despite known micro-outages. 

Your task is to implement a strict C-based input validator that acts as a gatekeeper for these uptime logs.

1. **Analyze the Alert:**
   An automated monitoring graph generated an alert image at `/app/graph_alert.png`. Use an OCR tool like `tesseract` to read the text in this image. It contains the exact validation rules and precision-loss constraints you need to implement.

2. **Fix the Build:**
   A skeleton of the validator exists at `/home/user/sanitizer.c` with a strict `/home/user/Makefile`. Currently, it fails to build due to a compilation error. Diagnose and fix the build failure so `make` successfully produces the executable `/home/user/sanitizer`.

3. **Implement the Validator (`/home/user/sanitizer.c`):**
   The program must read exactly one line from standard input containing three space-separated tokens:
   `[filename] [uptime_seconds] [total_seconds]`
   
   Example: `db-server-01 86399.5 86400.0`

   The program must exit with status `0` (clean/accept) if the input perfectly adheres to the rules found in the alert image. It must exit with status `1` (evil/reject) if:
   - The filename contains spaces, shell metacharacters, or violates the allowed character set (which causes our downstream shell scripts to break).
   - The metric values trigger the floating-point precision loss condition described in the image.
   - The values are logically invalid (e.g., uptime > total).

4. **Verify against the Corpora:**
   To test your validator, two directories of test logs are provided:
   - `/app/clean/`: Contains logs that must be **accepted** (exit code 0).
   - `/app/evil/`: Contains logs that must be **rejected** (exit code 1).
   
   Ensure your compiled `/home/user/sanitizer` correctly classifies 100% of the files in both directories when their contents are piped to standard input. Do not modify the corpora files.