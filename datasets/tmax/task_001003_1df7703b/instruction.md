You are an automation specialist building a text processing pipeline. We are receiving raw character streams from a legacy sensor system that frequently drops data packets. You need to write a Go program that acts as a quality gate and gap-filler for these streams.

First, extract the processing configuration from the image located at `/app/sensor_config.png`. This image contains critical parameters for the gap-filling logic, such as the missing character indicator, the maximum allowed forward-fill length, and the fallback character for unfillable gaps. You may use `tesseract` to read it.

Your objective is to write a Go program at `/home/user/process_stream.go` and compile it to an executable at `/home/user/process_stream`. 

The executable must behave exactly as follows:
1. It reads a single line of text from Standard Input (stdin).
2. **Validation Checkpoint:** It verifies that the input string consists strictly of uppercase alphabetic characters (`A-Z`) and the missing character indicator specified in the image. If any invalid characters are present, or if the string is empty, the program must immediately print "INVALID" to standard output and exit with status code 1.
3. **Resampling and Gap-filling:** For valid strings, the program scans from left to right. When it encounters the missing character indicator, it performs a "forward fill" by replacing the missing character with the most recently observed valid alphabetic character.
4. **Constraint Enforcement:** A forward fill can only be applied up to the maximum consecutive times specified in the image's `MAX_FILL` setting. If a gap exceeds this length, the remaining missing characters in that specific gap must be replaced by the `FALLBACK_CHAR` specified in the image.
5. If the string starts with missing characters (i.e., there is no preceding valid character to forward-fill from), those initial missing characters cannot be forward-filled and must be replaced by the `FALLBACK_CHAR`.
6. The program prints the final transformed string to Standard Output (stdout) without any additional formatting or trailing newline (unless provided in the input, but strip the newline for processing), and exits with status code 0.

Ensure your code is highly robust. It will be aggressively tested against thousands of randomly generated streams to verify bit-exact output equivalence.