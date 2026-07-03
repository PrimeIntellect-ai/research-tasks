You are a DevOps engineer analyzing a failing log processing pipeline written in C. Recently, the legacy log processor started crashing silently or calculating incorrect exponentially moving averages (EMA) due to malicious or corrupted log entries triggering a signed integer overflow.

Your task is to debug the system, extract the corrupted states, and build a robust C-based log sanitiser. 

Complete the following steps:

1. **Extract System Parameters (Image Fixture):**
   The original design specifications for the log processor's limits and convergence formulas were lost, but a screenshot of the design doc remains at `/app/config_params.png`. Use an OCR tool (like `tesseract`) to extract the correct `EMA_ALPHA` multiplier and the `MAX_PAYLOAD` integer limit from this image.

2. **Memory Dump Analysis:**
   Yesterday, the system suffered a silent crash. A raw memory dump was captured at `/app/memory.dmp`. Analyze this dump using standard shell utilities to find the exact 32-character hexadecimal transaction ID that caused the crash. The ID is clearly prefixed with `CRASH_TX:`. 
   Save ONLY the 32-character ID (without the prefix) into `/home/user/crash_tx.txt`.

3. **Build the Adversarial Log Sanitiser:**
   Write a C program at `/home/user/sanitiser.c` and compile it to `/home/user/sanitiser`.
   This utility must take exactly one CLI argument: the path to a log file to check (e.g., `./sanitiser log.txt`).
   
   The sanitiser must read the file and determine if it is "clean" or "evil" based on the following rules:
   * **Rule 1:** If the file contains the exact crash transaction ID you extracted in Step 2, it is EVIL.
   * **Rule 2:** The logs contain a payload size marker formatted as `SIZE:<number>`. Due to an x86 integer overflow bug in the downstream legacy system, any log where the `<number>` is strictly greater than the `MAX_PAYLOAD` value found in the image, OR is negative, is EVIL.
   * If neither rule is violated, the log is CLEAN.
   
   Your compiled program must:
   * Return exit code `0` if the file is cleanly validated.
   * Return exit code `1` if the file is identified as evil.

You can verify your sanitiser against the test corpora provided in `/home/user/corpora/clean/` and `/home/user/corpora/evil/`. Your sanitiser must correctly classify 100% of the files in both directories.