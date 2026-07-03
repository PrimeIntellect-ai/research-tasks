You are a mobile build engineer maintaining the CI pipelines for a cross-platform mobile application. 

We have a Python build script located at `/home/user/mobile_pipeline/build_lookup.py` that pre-computes a sine lookup table (a core numerical algorithm used by our mobile game engine) and generates a C header file. 

To simulate cross-compilation on our x86 CI runners, we use a custom emulator module `mobile_emulator.py`. When the environment variable `TARGET_ARCH=arm64` is set, `mobile_emulator.py` automatically monkey-patches Python's `math` module to simulate the lower-precision NEON floating-point characteristics of our target mobile devices.

Currently, the test suite passes locally but fails in CI:
Locally (x86_64):
```bash
cd /home/user/mobile_pipeline
python build_lookup.py
python test_lookup.py  # Passes
```

In CI (ARM64 simulated cross-compilation):
```bash
cd /home/user/mobile_pipeline
TARGET_ARCH=arm64 python build_lookup.py
TARGET_ARCH=arm64 python test_lookup.py  # FAILS!
```

A recent commit ran an auto-formatter that alphabetically sorted the imports in `build_lookup.py`. We suspect this broke the import ordering, causing the script to cache the standard high-precision `math.sin` *before* the emulator had a chance to monkey-patch it.

Your task:
1. Identify and fix the import ordering bug in `/home/user/mobile_pipeline/build_lookup.py` so that the `mobile_emulator` correctly applies its patches to `math.sin` before it is imported or used by the build script.
2. Regenerate the header file by running `TARGET_ARCH=arm64 python build_lookup.py`.
3. Verify the fix by running `TARGET_ARCH=arm64 python test_lookup.py` to ensure it outputs `PASS`.

Leave the final, corrected `/home/user/mobile_pipeline/build_lookup.py` in place, along with the successfully generated `/home/user/mobile_pipeline/lookup_arm64.h`. Do not modify `test_lookup.py` or `mobile_emulator.py`.