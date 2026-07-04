You are an artifact manager responsible for curating our custom binary backup repositories. We recently lost the source code for our primary decompression utility, but we managed to recover a scanned design document that describes the custom compression format used for our binary artifacts.

Your task is to write a Python 3 script that accurately implements the decompression algorithm described in the recovered design document. 

Here are your instructions:
1. Locate the scanned format specification image at `/app/format_spec.png`.
2. Extract the rules for the custom "ArtePak RLE" compression algorithm from the image. 
3. Write a Python script at `/home/user/custom_decompress.py` that performs this decompression. 
   - The script must read the compressed binary stream from `stdin`.
   - The script must write the raw, uncompressed binary data directly to `stdout`.
   - Ensure you handle binary I/O properly without unwanted string encoding/decoding.
   - The script must exit cleanly (exit code 0) upon reaching EOF.

The automated verification system will test your script by feeding it thousands of randomly generated compressed streams and comparing its binary output against our legacy compiled binary oracle. Your script must be bit-exact in its output.