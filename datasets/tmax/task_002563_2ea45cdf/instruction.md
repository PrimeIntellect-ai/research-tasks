You are a security researcher analyzing a suspicious binary that leaves obfuscated logs on compromised Linux machines. The malware attempts to hide its tracks by subtly manipulating log timestamps, which causes standard forensic tools to misinterpret the sequence of events. 

Your goal is to fix our internal timeline reconstruction tool and build a malware log detector.

**Step 1: Extract the Sync Seed**
We recovered a screenshot from the threat actor's machine at `/app/evidence.png`. Use standard OCR tools (e.g., `tesseract`) to extract the text from this image. It contains a critical `SYNC_SEED` (a floating-point multiplier) used by the malware's time obfuscation routine.

**Step 2: Fix the Timeline Parser**
We have a draft Go script at `/home/user/timeline.go` that attempts to reconstruct the timeline across three different services. However, it crashes due to an infinite recursion/loop termination bug in its custom sorting logic. Furthermore, when it parses the floating-point epoch timestamps (`seconds.microseconds`), it suffers from numerical instability, causing timezone drifts to accumulate incorrectly.
Fix `/home/user/timeline.go` so that it safely parses the logs, correctly applies the timezone offsets without floating-point drift, and sorts them chronologically.

**Step 3: Build the Detector**
Using the insights from the fixed timeline tool and the `SYNC_SEED` from the image, write a new Go program at `/home/user/detector.go`. 
This program must take a single file path as a command-line argument:
`go run /home/user/detector.go <path_to_log_file>`

The detector should read the log file, parse the timestamps, apply the `SYNC_SEED` multiplier to the drift, and determine if the log file contains malware-injected entries. 
* If the log file is benign, the program must print EXACTLY the string `CLEAN` to standard output.
* If the log file contains malware tampering (where the corrected timestamps travel backwards in time by more than 500ms), it must print EXACTLY the string `EVIL` to standard output.

To ensure your detector is robust, we have provided an adversarial corpus of log files:
* `/app/corpus/clean/` contains benign system logs.
* `/app/corpus/evil/` contains malware-tampered logs.

Your `detector.go` must successfully classify all files in both directories.