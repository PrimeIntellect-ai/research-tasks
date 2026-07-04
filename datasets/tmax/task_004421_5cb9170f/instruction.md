You are tasked with debugging a critical regression in a vendored serialization library and creating a robust sanitization filter to prevent future data corruption.

We have a vendored C++ package located at `/app/libsensordata`. It is a library used to serialize and deserialize high-precision telemetry data. Recently, our downstream systems have been experiencing severe precision loss and encoding crashes when processing certain payloads.

Your task consists of three phases:

**Phase 1: Bisection and Root Cause Analysis**
The regression was introduced somewhere in the last 200 commits of the `main` branch in `/app/libsensordata`.
- The commit tagged `v1.1.0` is known to be GOOD.
- The `HEAD` of the `main` branch is known to be BAD.
- You must use `git bisect` to identify the exact commit that introduced the precision loss regression. You can write a small script to automate the bisection by checking if serializing and deserializing a `double` value (e.g., `123456789.123456789`) maintains its exact precision using the library's `Telemetry::serialize()` and `Telemetry::deserialize()` methods.

**Phase 2: Fix the Vendored Package**
Once you have identified the offending commit, you will see it introduced a flawed data transformation (likely related to how 64-bit floats are packed, or an incorrect cast). 
- Fix the bug in the library's source code so that full `double` precision is maintained and encoding errors are avoided.
- Recompile the library using `make` in `/app/libsensordata`. Ensure `make check` passes.

**Phase 3: Create an Adversarial Payload Detector**
Because we ingest data from untrusted sensors, we need a proactive filter. We have provided two corpora of raw payload files:
- `/app/corpora/clean/`: Contains 50 valid, well-formed telemetry files.
- `/app/corpora/evil/`: Contains 50 adversarial or malformed telemetry files designed to trigger NaN poisoning, extreme precision truncation, or broken UTF-8 encoding paths in the ingestion pipeline.

You must write a C++ program located at `/home/user/detector.cpp` and compile it to `/home/user/detector`.
- The executable must take a single command-line argument: the path to a payload file.
- Example invocation: `/home/user/detector /app/corpora/evil/payload_01.dat`
- The detector must inspect the file and **accept** valid payloads by returning an **exit code of 0**.
- The detector must **reject** malformed/adversarial payloads by returning an **exit code of 1**.
- Your detector must achieve 100% accuracy: 100% of the clean corpus must be accepted, and 100% of the evil corpus must be rejected.

Ensure your compiled `detector` binary is executable and strictly adheres to the exit code requirements, as an automated grading script will iterate over both corpora to evaluate your solution.