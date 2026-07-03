You are an IT support technician investigating a failed nightly build on a Linux build server. The system crashed hard, leaving behind a few artifacts. 

The developer who submitted the ticket reported: "The build failed with a linker error, but the logs are huge. The crash also corrupted our build state tracking journal and left a raw memory dump. I need to know the ID of the last successfully committed module, the exact memory error code it produced during the crash, and the name of the missing function that caused the linker to fail."

You need to analyze the following files in `/home/user/`:
1. `/home/user/state.journal`: A partially corrupted write-ahead log. Find the ID of the LAST module that was explicitly marked as "commit" before the file becomes corrupted binary garbage. (Format is `[WAL] commit module <ID>`).
2. `/home/user/build_mem.dump`: A raw memory dump from the crashed process. Once you have the module ID from step 1, search this binary file to extract its specific error code. The memory contains a string in the format `MODULE_ID: <ID> ERROR_CODE: <ERROR_CODE>`.
3. `/home/user/compiler_logs.txt`: A massive log of compiler output. Find the linker error (`undefined reference`) associated with that specific module ID, and extract the exact name of the missing function (the function name inside the single quotes).

Create a file at `/home/user/resolution.txt` containing exactly these three lines, replacing the bracketed values with what you found:
Module: [ID]
ErrorCode: [ERROR_CODE]
MissingFunction: [FUNCTION_NAME]

Do not include any other text in the file.