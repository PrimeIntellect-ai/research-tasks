You are tasked with debugging a failing build script that handles parallel asset compilation for our CI system. 

The script is located at `/home/user/build.sh`. When we run it with a high number of assets (e.g., `./build.sh 50`), it behaves unpredictably. Sometimes it completes successfully, but often it fails to output the correct final count, or worse, it hangs indefinitely and we have to cancel the CI pipeline. When it hangs, we notice that `/home/user/build.log` grows extremely large with repetitive error messages.

Your task is to:
1. Diagnose the cause of the intermittent failures (which seem to be related to concurrent state updates).
2. Fix the concurrency bug so that the final state count is always strictly equal to the number of input assets.
3. Diagnose and fix the issue causing the script to hang indefinitely (infinite loop) when verification fails.

Modify `/home/user/build.sh` in-place so that it correctly and reliably processes the given number of assets concurrently, finishes successfully, prints `Success: <N>`, and exits with code 0. 

Requirements:
- Do not remove the backgrounding of processes (`&`) in the main loop; the compilation must remain parallel.
- Do not use external databases; standard Linux tools and shell built-ins are required.
- The script must reliably complete ` ./build.sh 50 ` within 5 seconds without hanging.