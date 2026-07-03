You are a performance engineer tasked with optimizing a critical data deserialization component. We have a legacy binary, `/app/legacy_decoder`, which decodes a custom run-length-encoded (RLE) hexadecimal format. Unfortunately, the source code is lost, the binary is stripped, and it suffers from severe performance bottlenecks and occasional assertion failures on deeply nested data.

We have recovered a design schematic for the custom encoding format, located at `/app/format_schematic.png`. You will need to use basic OCR or visual analysis to extract the format rules from this image. 

Your objective is to:
1. Analyze `/app/format_schematic.png` to understand the encoding rules and serialization structure.
2. Reverse engineer the behavior of `/app/legacy_decoder` to understand how it handles edge cases (you can run it to observe tracebacks and outputs on various inputs).
3. Write a highly optimized, bug-free C++ implementation of the decoder.
4. Save your C++ source code to `/home/user/fast_decoder.cpp` and compile it to `/home/user/fast_decoder`.

Your program `/home/user/fast_decoder` must accept exactly one command-line argument (the encoded string) and print the decoded raw bytes as a hex string to standard output, followed by a newline. It must not crash on malformed inputs; instead, it should print "INVALID" and exit with code 1.

Your implementation must be bit-exact equivalent in its successful outputs to our internal reference oracle, but without the performance bottlenecks. An automated system will fuzz your compiled binary against the oracle with thousands of inputs to ensure perfect compatibility.