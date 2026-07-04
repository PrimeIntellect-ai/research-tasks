I have a compiled, stripped Linux binary located at `/app/conf_oracle` that acts as our legacy configuration change tracker. It processes incoming configuration deltas from `stdin` and writes aggregated tracking data to `stdout`. 

We need to rewrite this tool in **Rust** because the legacy C code is unmaintainable, but the new tool must be **bit-exact equivalent** to the old binary so it can drop directly into our pipeline DAG orchestration.

**Your Goal:**
Write a Rust program in `/home/user/tracker/` that compiles to `/home/user/tracker/target/release/tracker`. It must read from `stdin` and write to `stdout` matching the exact behavior of `/app/conf_oracle`.

**High-Level Algorithm of the Oracle:**
1. **Input Parsing:** Reads line-by-line from `stdin`. Each line is formatted as `KEY PAYLOAD` (separated by a single space). `KEY` is an alphanumeric string. `PAYLOAD` is an arbitrary UTF-8 string containing multi-language text.
2. **Unicode Normalization:** The `PAYLOAD` is immediately normalized to Unicode Normalization Form C (NFC).
3. **Hash-based Deduplication:** The system computes the SHA-256 hash of the NFC-normalized `PAYLOAD`. If a payload with this exact hash has already been processed for this specific `KEY`, the line is ignored (no output, no state update).
4. **Rolling Statistics:** For each `KEY`, the system maintains a rolling history of the lengths (in **Unicode scalar values/characters**, not bytes) of the last 3 unique accepted NFC payloads.
5. **Output:** Every time a new unique payload is accepted for a `KEY`, it calculates the integer average (floor division) of the character lengths in that key's rolling window (up to 3 items). It then prints to `stdout`: `{KEY}:{ROLLING_AVG}\n`.

**Example:**
If the input is:
```
APP1 setting=true
APP1 setting=true
APP1 lang=es,val=niño
APP2 init
```
The output of your Rust program must perfectly match the output of `/app/conf_oracle` given the same input.

Please initialize a Cargo project, implement the logic, and ensure it builds in release mode at the requested path. You can test your implementation by running random inputs through both your binary and `/app/conf_oracle` and comparing the outputs.