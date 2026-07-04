You are an Artifact Manager responsible for curating binary repositories. We are migrating our systems to a new custom artifact format (`.artx`). However, our ingestion pipeline has been flooded with malformed and malicious artifacts. 

Your task is to write a Python classifier and processor script that validates, decompresses, and securely writes the metadata of these artifacts.

We have a directory of test artifacts. Your script must correctly reject the malicious ones and successfully process the clean ones.

**Artifact Format Specification (.artx):**
1. **Magic Bytes:** The first 4 bytes must be exactly `ARTX` (ASCII).
2. **Watermark:** The next 16 bytes contain a strict security watermark (ASCII). The exact 16-character string you must check against is embedded in the image file located at `/app/watermark.png`. You must extract this text from the image to hardcode the check in your script.
3. **Metadata Size:** The next 4 bytes are a 32-bit little-endian integer representing the *uncompressed* size of the JSON metadata.
4. **Metadata Payload:** The remainder of the file is the JSON metadata, compressed using a custom Run-Length Encoding (RLE). 
   - The RLE format consists of pairs of bytes: `[count][character]`.
   - `count` is a 1-byte unsigned integer (1-255) representing how many times to repeat the `character`.
   - `character` is a 1-byte ASCII character.
   - Example: `0x03 0x41` decodes to `AAA`.

**Validation Rules:**
An artifact must be REJECTED if any of the following are true:
- The magic bytes do not match `ARTX`.
- The watermark does not perfectly match the 16-character string extracted from `/app/watermark.png`.
- The RLE decoding terminates unexpectedly (e.g., incomplete pair).
- The uncompressed size of the decoded metadata does NOT exactly match the length declared in the header.
- The decoded metadata is not perfectly valid JSON.
- The decoded JSON object does NOT contain the key `"artifact_id"`.

**Your Deliverable:**
Write a Python script at `/home/user/curator.py`. 
It must take exactly two command-line arguments: an input `.artx` file path, and an output JSON file path.
`python3 /home/user/curator.py <input_file> <output_file>`

- **If the input artifact is VALID (Clean):** You must decode the JSON metadata and save it to `<output_file>`. To prevent file corruption during processing crashes, you **must use an atomic write pattern**: write the JSON to a temporary file in the same directory as the target, and then atomically rename it to `<output_file>`. The script must exit with status code `0`.
- **If the input artifact is INVALID (Evil):** The script must exit with a non-zero status code (e.g., `1`) and must NOT create the final `<output_file>`.

The automated verifier will test your script against a hidden corpus of clean and evil files.