I am a developer trying to debug a failing build process for my project located at `/home/user/project`. The build is currently failing for two distinct reasons, and I need your help to fix the environment and scripts so the build passes.

Here is the situation:
1. Yesterday, our asset compiler crashed and left a memory dump file at `/home/user/project/core.dump`. The memory dump contains a string starting with `FATAL_ERROR:` which points to the absolute path of a corrupted asset file. 
2. You need to analyze this memory dump, extract the `FATAL_ERROR` string, and identify the corrupted file.
3. The identified corrupted asset file is filled with invalid non-printable binary characters (like null bytes) interspersed with valid text. Clean this specific asset file by removing all non-printable characters (keep only standard printable ASCII characters). Save the cleaned content back into the exact same file path.
4. Our pre-build script, `/home/user/project/calculate_threshold.sh`, reads weights from a text file and sums them using `awk`. However, floating-point precision loss in `awk` is causing it to output `0.30000000000000004` instead of the expected `0.3`, causing a strict string equality check to fail. Fix the `awk` command in this script so it outputs the sum rounded to exactly one decimal place.
5. Once you have cleaned the asset file and fixed the bash script's precision loss, run the main build script: `/home/user/project/build.sh`.

Redirect the standard output of the successful `build.sh` run to `/home/user/project/build_success.log`. 

Please execute the necessary commands to diagnose and resolve these issues.