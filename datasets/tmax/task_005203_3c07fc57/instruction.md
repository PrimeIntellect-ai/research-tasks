You are a DevOps engineer investigating a crashing log parser service. The container orchestrator reported that the service exited with a Segmentation Fault. 

An automated cleanup script deleted the problematic log file before the container died, but we managed to snapshot the small volume it was stored on as an ext4 disk image located at `/home/user/logs.img`.

Your tasks:
1. **Recover the deleted file**: Inspect `/home/user/logs.img` to find and recover the deleted file originally named `corrupt_record.log`. Save its contents to `/home/user/recovered.log`.
2. **Diagnose and Fix**: The source code for the parser is at `/home/user/parser.c`. It has a format parsing vulnerability that crashes when it encounters the edge-case data in the recovered log. Fix the vulnerability in `/home/user/parser.c` so that it parses the data safely without segfaulting or crashing. Ensure it can still compile via `gcc -o parser parser.c`.
3. **Regression Test**: Create an executable bash script at `/home/user/regression_test.sh`. This script must:
   - Compile `/home/user/parser.c` to `/home/user/parser`.
   - Run the compiled `parser` against `/home/user/recovered.log`.
   - Return an exit code of `0` if the run is successful (no crash), and a non-zero exit code if the compiler fails or the program segfaults.

Note: You may use the `sleuthkit` suite (e.g., `fls`, `icat`) to interact with the disk image.