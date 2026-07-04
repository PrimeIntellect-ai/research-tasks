Our legacy log processing service occasionally hangs or runs out of memory when processing certain user-supplied structured logs. We've traced the issue to an infinite loop and memory explosion in our recursive parser when it encounters deeply nested or malformed structures.

You need to create a pre-filter classifier to block these "evil" payloads before they reach the parser. 

Here is what you need to do:
1. **Analyze the System Limits:** There is an architecture diagram at `/app/system_diagram.png`. You must extract the strict maximum parsing depth limit written on this diagram (you can use `tesseract` to read it).
2. **Understand the Format:** The payloads consist of nested braces `{}`. A payload is considered "safe" (clean) if and only if:
   - All braces are perfectly balanced and properly closed.
   - The maximum nesting depth of the braces does NOT exceed the limit specified in the system diagram.
   - Any payload that violates these rules is "unsafe" (evil).
3. **Build the Detector:** Create a Python script at `/home/user/detector.py` that takes a single file path as a command-line argument. 
   - The script must read the contents of the file.
   - It must exit with code `0` if the payload is safe.
   - It must exit with code `1` if the payload is unsafe.

We will test your `detector.py` script against a large hidden dataset of clean and evil payloads.