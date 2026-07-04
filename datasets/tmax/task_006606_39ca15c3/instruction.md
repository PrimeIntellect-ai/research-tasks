You are an operations engineer triaging Incident #104. A critical C-based data processing daemon has crashed, and the pipeline is currently halted. 

Your workspace is located at `/home/user/incident-104`.

Here is the situation:
1. The daemon executable `data_processor` is failing to start. You suspect it is missing a required initialization file, but the error message is unhelpful. Use system call tracing to determine the exact absolute file path the binary is attempting (and failing) to open on startup.
2. The previous daemon instance crashed and left a memory dump at `/home/user/incident-104/core`. The missing initialization file must contain a specific 16-character authentication token (starting with `TOKEN_`) that was loaded in memory during the crash. Extract this token from the memory dump and write it into the missing file path you discovered in step 1.
3. Once the daemon can start, it will process data incorrectly due to a known mathematical bug. The original developer has provided a patch for the source code (`processor.c`) at `/home/user/incident-104/patch.diff`. Apply this patch.
4. Recompile the daemon using the provided `Makefile`. You will encounter a compilation/linker error because the patched code utilizes a mathematical function without properly linking the required standard math library. Resolve this error (either by modifying the Makefile or running the corrected compilation command manually).
5. Run the newly compiled `data_processor`. It will output a successful completion hash.

Save the final completion hash (exactly as output by the program, e.g., `SUCCESS_HASH_...`) to a new file at `/home/user/incident-104/resolution.txt`.