You are a security researcher analyzing a suspicious process memory dump. Your goal is to extract the hidden Command and Control (C2) configuration and identify a parsing vulnerability in the provided analysis tools.

You have been provided with a directory `/home/user/investigation` containing:
1. `memdump.bin` - A simulated process memory dump containing the obfuscated C2 configuration.
2. `extractor.py` - A Python script written to parse config blocks from the memory dump and iteratively decode the C2 address.
3. `fuzz_corpus.txt` - A list of generated inputs that are known to cause a crash in `extractor.py`.

However, `extractor.py` has a few issues:
- **Format Parsing Edge-Case**: The function `parse_config_block` searches for the signature `C2CFG{` and attempts to read a length field immediately after. It crashes if the payload contains unexpected null bytes or malformed length markers due to a strict ASCII decoding assumption. You need to repair this so it safely ignores or handles non-ASCII bytes without throwing a `UnicodeDecodeError`.
- **Convergence Failure**: The `decode_c2` function iteratively applies a base64-like decoding step until the string stops changing. However, due to a bug in how padding is handled, certain payloads cause an infinite loop (it oscillates between states). Fix the convergence failure so the loop terminates correctly when a valid, unchanging C2 URL (starting with `http://` or `https://`) is found, or it hits a maximum of 10 iterations.

Your tasks:
1. Fix the bugs in `extractor.py`.
2. Run the fixed `extractor.py` on `memdump.bin` to successfully extract the final C2 URL. Save this exact URL to `/home/user/investigation/c2.txt`.
3. The script crashes on some inputs in `fuzz_corpus.txt` with a `ValueError: Corrupt Header`. Use delta debugging / test minimization techniques to find the **minimal** string from the crashing input in `fuzz_corpus.txt` that still triggers the exact `ValueError: Corrupt Header` exception in the *original* (unfixed) `parse_config_block` logic. 
4. Save this minimal crashing string (just the characters required to trigger the crash) to `/home/user/investigation/minimal_crash.txt`.

Ensure your fixes in `extractor.py` are robust. The final `/home/user/investigation/c2.txt` must contain only the decoded URL, and `/home/user/investigation/minimal_crash.txt` must contain the minimized string.