You are tasked with porting and updating a URL routing state machine validator for a CI pipeline.

Recently, our routing test suite started failing in CI because the allowed path-transition cycle was updated, but the validator tool wasn't. The old validator is written in Rust (`/app/legacy_validator.rs`), but it currently fails to compile due to a borrow checker error, and it enforces the old legacy cycle order.

Your objective is to write a new Python-based utility from scratch at `/home/user/url_sanitizer.py` that filters out invalid URL routing paths based on the new state machine.

**Requirements:**
1. **Analyze the Video Fixture:** The new, correct routing state cycle is documented visually in `/app/sequence.mp4`. This video contains exactly 3 distinct solid-color frames. 
   - Extract the frames and determine their colors. 
   - Map each color to its lowercase English name (`red`, `green`, `blue`).
   - The temporal order of these frames in the video dictates the **only** valid cyclical state transition sequence for URL paths (e.g., if the video shows ColorA -> ColorB -> ColorC, then a path must follow ColorA -> ColorB -> ColorC -> ColorA ...).

2. **Translate & Fix Logic:** Review the broken `/app/legacy_validator.rs` to understand how URLs are structured and parsed. Re-implement the parsing logic in Python, but apply the correct state transition cycle you extracted from the video instead of the old one. 

3. **Write the Sanitizer Utility:**
   - Create a script at `/home/user/url_sanitizer.py`.
   - It must take two positional arguments: an input file path and an output file path.
   - Invocation: `python3 /home/user/url_sanitizer.py <input_file> <output_file>`
   - The input file will contain one URL path per line (e.g., `/api/v1/route/red/green`).
   - The script must evaluate the path segments. Segments that are NOT one of the 3 state colors should be ignored for the purpose of state validation.
   - If the sequence of state colors in the URL strictly follows the cycle demonstrated in the video (starting at any valid state), the URL is considered **valid**.
   - If there is any invalid state transition (e.g., skipping a state, going backwards, or repeating the same state consecutively), the URL is considered **invalid**.
   - Write ONLY the valid URLs to the `<output_file>`, preserving their exact original line format. Drop the invalid URLs.

Two test corpora have been provided for you to test your script locally:
- `/app/corpus/clean/`: Contains text files with 100% valid URLs.
- `/app/corpus/evil/`: Contains text files with malicious/invalid state transitions.

Ensure your Python script successfully preserves all lines from the clean corpus and drops all lines from the evil corpus.