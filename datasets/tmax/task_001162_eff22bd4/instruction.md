You are an infrastructure engineer investigating a memory leak in a critical long-running audio processing service.

The service uses a custom C-extension for Python to quickly parse WAV file headers. 
Your tasks:

1. **Build Failure Diagnosis:** The source code for the service is in `/home/user/audioproc`. If you run `python3 setup.py build_ext --inplace`, it fails to build due to a configuration error. Diagnose the build failure, modify the build configuration or code as needed, and successfully compile the extension.

2. **System Call Tracing & Root Cause Analysis:** Once built, you can run the service wrapper `python3 run_service.py <path_to_wav>`. We have provided an audio file at `/app/trigger.wav`. When the service processes this specific file, it exhibits a severe memory leak. Use system call tracing tools (like `strace`) and code comprehension on the C-extension to determine exactly what malformed property of `/app/trigger.wav` causes the leaked allocations (e.g., an un-freed buffer on a specific parsing branch).

3. **Adversarial Corpus Filter:** You cannot deploy a fix to the C-extension in production right now. Instead, you must write a Python pre-filter script at `/home/user/filter.py` that takes a single file path as an argument.
   - Usage: `python3 /home/user/filter.py <path_to_wav>`
   - The script must parse the WAV file safely (using standard Python libraries like `struct` or `wave`, do NOT use the buggy C-extension).
   - If the file is "clean" (safe to process), the script must exit with status code `0`.
   - If the file is "evil" (contains the property that triggers the memory leak), the script must exit with status code `1`.

We will verify your solution by running your `/home/user/filter.py` against a hidden dataset of clean and evil audio files.