You are a developer inheriting an unfamiliar, legacy data-processing system. The system uses a Python C-extension to interact with a proprietary static library, but the original developers left it in a broken state. It crashes frequently and cannot even be rebuilt from source.

Your task consists of four phases:

1. **Log Inspection:** Inspect `/home/user/legacy_app/crash.log`. The previous system crashed when processing a specific anomalous hex payload. Find this payload.
2. **Compiler and Linker Error Interpretation:** The C-extension source code is in `/home/user/legacy_app/processor.c` and is built using `/home/user/legacy_app/setup.py`. Attempting to run `python3 setup.py build_ext --inplace` fails with an "undefined reference" linker error. Fix `setup.py` so that it correctly links against the static library `/home/user/legacy_app/libmagic.a`. 
3. **Binary Reverse Engineering:** Even after fixing the linker flags, the build fails because `processor.c` is calling the wrong function name. Use binary inspection tools (like `nm` or `strings`) on `/home/user/legacy_app/libmagic.a` to find the correct exported symbol for processing payloads (it will be a variation of `process_payload`). Modify `processor.c` to declare and call this correct function.
4. **Minimal Reproducible Example:** Once the extension compiles successfully into a `.so` file, write a Python script at `/home/user/legacy_app/mre.py`. This script should:
   - Import the newly compiled `processor` module.
   - Convert the anomalous hex payload found in `crash.log` into bytes.
   - Pass these bytes to `processor.run(payload)`.
   - Write the exact string returned by the function to `/home/user/legacy_app/result.txt`.

Ensure your `mre.py` script runs successfully and creates `result.txt` with the correct output.