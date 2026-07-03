As a technical writer organizing our company's documentation, I need to recreate our legacy documentation processing pipeline. We lost the original source code, but I found a screenshot of the specification document at `/app/doc_rules.png`.

I need you to:
1. Extract the processing rules from the image `/app/doc_rules.png`. 
2. Create a Python script at `/home/user/stream_processor.py` that implements these exact rules.
3. The script must read from `stdin` and write to `stdout` (streaming I/O). 
4. The script must be executable (`chmod +x`).

The script needs to be highly robust as it will be used to process thousands of files by piping them through standard input. Ensure you handle the exact text formatting rules specified in the image perfectly, as our automated manifest and checksum validation system relies on bit-exact output.

You have access to `tesseract` if you need it to read the image. Please create the Python script so it exactly matches the intended behavior.