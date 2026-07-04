I am debugging a failing build for our distributed physics engine. The build pipeline keeps stalling in a "deadlock" state because the downstream nodes are receiving malformed, low-precision numeric data from our pre-processor, causing them to hang while waiting for convergence. 

To fix this, you need to reconstruct the correct pre-processing script. Unfortunately, the developer who originally wrote it accidentally deleted the reference data file from their local build filesystem before pushing.

Here is what you need to do:

1. **Recover the Reference Data**: There is an unmounted ext4 filesystem image at `/app/build_fs.ext4`. The developer accidentally deleted a file named `offsets.dat` from the root of this filesystem. You must recover the contents of this deleted file. It contains a single floating-point offset value on the first line.
2. **Read the Formatting Specs**: The exact floating-point precision and parsing rules are documented in a screenshot taken by the developer, located at `/app/specs.png`. You will need to extract the text from this image to understand how edge-cases (like missing decimals or scientific notation) should be handled.
3. **Write the Pre-processor**: Create a Bash script at `/home/user/format_parser.sh`. The script must read a stream of raw numerical strings from standard input (one per line). 
   - For each input, it must parse the number, add the offset value you recovered from `offsets.dat`, and repair the floating-point precision.
   - It must format the output strictly according to the rules you extracted from `/app/specs.png`.
   - The script must use standard Bash tools (like `awk`, `bc`, `sed`) to perform the math and formatting.
   - Make sure your script is executable (`chmod +x`).

The automated build verifier will test your script by feeding it thousands of randomly generated edge-case inputs (e.g., `1.0e-4`, `42`, `.999`, `-0.0`) and comparing your script's output bit-for-bit against a proprietary reference binary. 

Please ensure your script perfectly matches the expected behavior so we can unblock the build pipeline!