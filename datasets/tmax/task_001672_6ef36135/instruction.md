Wake up! It's 3:00 AM and you've just been paged. Our primary telemetry ingestion service crashed violently due to an out-of-memory error. The system uses a high-performance JSON library and writes incoming telemetry to a custom Write-Ahead Log (WAL) before flushing to the database.

Here is the situation:
1. **Broken Dependency:** We were in the middle of rolling out a local build of the `ultrajson` library when the server went down. The source is located at `/app/ultrajson`. However, the previous engineer left it in a broken state—it currently fails to compile due to what looks like compiler/linker errors. You need to diagnose the build failure, fix the package configuration, and successfully install the package into the current Python environment so that `import ujson` works.
2. **Corrupt WAL Recovery:** After fixing the dependency, you need to write a script to process recovered log entries. The WAL appends data in a proprietary frame format, but due to the crash, many frames have trailing garbage, incomplete data, or off-by-one length prefixes.
3. **Data Processor Script:** You must create a Python script at `/home/user/process_record.py` that processes single telemetry records. We have a legacy binary oracle we must perfectly emulate. 
   - Your script must accept a single command-line argument: a hex-encoded string representing a single, potentially malformed WAL frame payload.
   - It should attempt to decode the hex string.
   - It should search for the first occurrence of the character `{` and the last occurrence of `}`.
   - It should extract the string between these brackets (inclusive), parse it using the `ujson` library you just fixed, and print the resulting dictionary as a JSON string using Python's standard `json.dumps(..., sort_keys=True, separators=(',', ':'))`. 
   - If parsing fails or the brackets are missing, it should simply print `"INVALID_RECORD"`.

Make sure your `/home/user/process_record.py` precisely matches this behavior, as it will be exhaustively tested against our reference oracle using randomized fuzzy inputs to ensure absolute parity. 

Your goals:
- Fix the vendored `ultrajson` library and install it.
- Write `/home/user/process_record.py` exactly as specified.