You have inherited an unfamiliar, buggy C codebase located at `/home/user/data_processor`. 
Your goal is to fix the codebase so that it correctly compiles and processes data exactly as originally intended.

Here is what you need to do:
1. **Fix the build failure:** The codebase currently does not compile. Diagnose and fix the issue so that running `make` successfully builds the executable at `/home/user/data_processor/processor`.
2. **Recover the formula:** The current mathematical formula in the code is completely wrong. A design schematic for the system was saved as an image at `/app/schematic.png`. Use OCR (e.g., `tesseract`) or other tools to read the text from this image and implement the correct base formula.
3. **Recover the lost secret:** The formula in the schematic refers to an `OFFSET` value. This value was hardcoded in an early commit but was later accidentally overwritten and lost in the git history. Perform git history forensics to find the original numeric value of `OFFSET` and include it in your calculation.
4. **Fix the regression:** A recent commit introduced a regression in the bounds-checking logic. If an input is out of bounds, the program is supposed to exit with status code `2`. Use `git log` or `git bisect` to figure out what the correct bounds-checking logic was in the first working version, and restore it.

The program takes exactly 3 integer arguments (`A`, `B`, and `C`) via the command line, and prints a single integer to standard output.
When you are finished, ensure your code compiles into `/home/user/data_processor/processor`. 
Your final executable must be bit-exact equivalent in behavior (both output and exit codes) to the original reference logic.