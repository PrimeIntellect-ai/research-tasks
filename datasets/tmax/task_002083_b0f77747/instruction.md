You are a developer organizing a set of project files based on a custom binary index. The index contains the paths of required shared libraries for a CMake project, but your current Python script is failing to parse it correctly, consuming too much memory, and lacking proper tests.

Your workspace is in `/home/user/project/`.
There is a custom binary file `/home/user/project/index.bin`.
The file is a sequence of entries. Each entry is formatted as:
- 1 byte for encoding (0x01 for UTF-8, 0x02 for UTF-16LE)
- 2 bytes for the byte-length of the string (little-endian unsigned integer)
- N bytes of the actual encoded string data

You have a buggy script at `/home/user/project/organizer.py` that is supposed to read this file and output the file paths. 

Your tasks are:

1. **Character and Data Encoding**: 
   The `decode_entry(data, offset)` function in `organizer.py` currently ignores the encoding byte and assumes everything is UTF-8. Fix it so that it correctly reads the length, decodes the string using the specified encoding (0x01=utf-8, 0x02=utf-16le), and returns a tuple of `(decoded_string, next_offset)`.

2. **Property-Based Testing**:
   Create a test file `/home/user/project/test_organizer.py`. Use `pytest` and the `hypothesis` library to write a property-based test named `test_decode_encode`. 
   We have provided an `encode_entry(s, enc)` function in `/home/user/project/utils.py`. Your test must use `hypothesis.strategies.text()` to generate random strings, and `hypothesis.strategies.sampled_from([1, 2])` to generate the encoding byte. It should verify that passing the output of `encode_entry` into your fixed `decode_entry` (with an initial offset of 0) correctly recovers the original string.

3. **Memory Debugging**:
   The `read_index` function in `organizer.py` currently builds a massive string and does inefficient concatenations causing memory spikes. Refactor it to yield items as a generator or append them to a list efficiently. 
   Furthermore, import the `tracemalloc` module in `organizer.py`. Start tracing at the very beginning of the `main()` block. At the end of `main()`, get the peak memory usage (in bytes) and write just that integer to `/home/user/mem_peak.txt`.

4. **Output Generation**:
   Run your fixed `organizer.py` on `/home/user/project/index.bin`. Have it write the fully decoded list of file paths to `/home/user/organized_files.txt`. The list must be sorted alphabetically, with one file path per line.

Ensure your tests pass by running `pytest /home/user/project/test_organizer.py`.