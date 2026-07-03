You are a mobile build engineer maintaining a cross-platform data processing pipeline. You have been given a C source file and a patch that adds new features, but you must compile it carefully to maintain ABI stability and support multiple simulated target architectures.

Here are your instructions:
1. Navigate to `/home/user/telemetry_lib`. You will find `processor.c` and `update.patch`.
2. Apply `update.patch` to `processor.c` using standard patch utilities.
3. We need to ensure that internal helper functions do not pollute the shared library ABI. Create a linker version script at `/home/user/telemetry_lib/version.map` that exports **only** functions starting with the prefix `telemetry_` globally, and hides all other symbols (making them local).
4. Compile the patched `processor.c` into a shared library for Android named `libtelemetry_android.so`. You must compile it with the `-DTARGET_ANDROID` preprocessor flag, as a position-independent shared library, and apply your `version.map` script to the linker.
5. Compile the patched `processor.c` into a shared library for iOS named `libtelemetry_ios.so`. You must compile it with the `-DTARGET_IOS` preprocessor flag, as a position-independent shared library, and apply your `version.map` script to the linker.
6. Verify the ABI. Extract all exported, defined function symbols from `libtelemetry_android.so` that start with `telemetry_`. Sort them alphabetically and write exactly the symbol names (one per line) to `/home/user/android_exports.log`.
7. Repeat the extraction for `libtelemetry_ios.so` and write the sorted symbol names to `/home/user/ios_exports.log`.

Do not hardcode the log contents; use tools like `nm` to inspect the generated shared libraries and populate the logs. Ensure both `.so` files are located in `/home/user/telemetry_lib`.