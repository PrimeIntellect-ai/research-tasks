You are tasked with debugging and fixing a regression in a custom C-based serialization tool located at `/home/user/tlv_processor`. 

The tool decodes a custom Type-Length-Value (TLV) binary format. Recently, the automated nightly builds started timing out. We know the regression was introduced somewhere in the last 200 commits. The current `main` branch hangs indefinitely when processing a specific payload, whereas the tag `v1.0` works perfectly.

Your objectives:
1. **Isolate the regression:** Use `git bisect` to find the exact commit that introduced the infinite loop bug. The known good commit is tagged `v1.0`. The current `HEAD` (bad) is branch `main`. You will likely need to write a test script to automate the bisecting process since there are about 200 commits. 
2. **Diagnose and Fix:** Identify the root cause of the infinite loop in the TLV decoding logic. The bug involves incorrect intermediate state handling during the deserialization of a specific data type, causing loop termination to fail.
3. **Verify:** Fix the C code on the `main` branch so that it compiles and successfully processes the failing payload.
4. **Report:** Compile the fixed program and run it against `/home/user/payload.bin` (this file causes the hang on the buggy version). Save the standard output of the successful run to `/home/user/decoded_output.txt`. 

Finally, create a JSON file at `/home/user/bug_report.json` with the following precise structure:
```json
{
  "bad_commit_hash": "<full_40_char_git_hash_of_the_offending_commit>",
  "buggy_function_name": "<name_of_the_C_function_with_the_infinite_loop>",
  "decoded_payload_length": <integer_length_of_the_decoded_output_file_in_bytes>
}
```

Constraints & Notes:
- The binary is built by running `make` in `/home/user/tlv_processor`.
- The binary is executed via `./tlv_decoder <input_file>`.
- You may write whatever helper scripts (Python, Bash) you need to trace the state and automate `git bisect`.
- Ensure your fix correctly handles the edge case in the serialization format without breaking other types.