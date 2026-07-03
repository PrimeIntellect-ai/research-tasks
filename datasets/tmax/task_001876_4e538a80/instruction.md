You are a mobile build engineer responsible for maintaining a cross-platform polyglot pipeline. Recently, our automated build system started failing due to corrupted and maliciously crafted asset payloads crashing our native C/C++ mobile decoding libraries. 

We need to implement a robust Python-based filter to sanitize these assets before they reach the C++ compiler and asset packager.

**Step 1: Recover the Asset Specification**
The exact checksum parameters for our proprietary asset format were lost during a recent repository migration. However, we have a screenshot of the original specification document located at `/app/spec_fragment.png`. 
1. Use OCR (`tesseract` is installed) to read `/app/spec_fragment.png`.
2. Extract the custom **CRC-16 polynomial** (in hex) and the **XOR-out value** (in hex) from the image text.

**Step 2: Develop the Asset Sanitizer**
Create a Python script at `/home/user/filter.py` that validates an asset file. The script must take a single file path as a command-line argument:
`python3 /home/user/filter.py <path_to_asset_file>`

The script must exit with code `0` if the asset is perfectly valid (Clean), and exit with a non-zero code (e.g., `1`) if the asset is malformed or malicious (Evil).

An asset file is valid if and only if it meets ALL the following criteria:
1. **Encoding:** The entire file is valid, standard Base64 string data (no whitespace other than trailing newlines).
2. **Structure:** Once Base64 decoded, the binary data has a 4-byte header representing an unsigned 32-bit integer (Little Endian). This integer specifies the expected length of the *remaining* payload in bytes.
3. **Memory Safety:** The actual length of the remaining payload must exactly match the length specified in the header. (Malicious payloads often lie about this length to trigger buffer overflows in our C++ layer).
4. **Data Integrity:** A standard CRC-16 hash of the payload (excluding the 4-byte length header), computed using the polynomial and XOR-out value recovered from the image (assuming no XOR-in, standard shift direction, i.e., non-reflected input/output), must exactly match the last 2 bytes of the payload (Little Endian). 

**Step 3: Test against the Corpora**
We have provided a corpus of payloads to test your script:
- `/app/corpus/clean/`: Contains guaranteed valid assets.
- `/app/corpus/evil/`: Contains malformed assets (bad Base64, header mismatch, failed checksums, or trailing garbage).

Your script must accept 100% of the `clean` corpus and reject 100% of the `evil` corpus.

**Constraints:**
- Use Python 3. You may use standard library modules only (e.g., `base64`, `struct`, `sys`).
- You are strictly evaluated on your script's performance against the adversarial corpus.