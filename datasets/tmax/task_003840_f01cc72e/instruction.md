I need you to build a C++ data cleaning utility for our pipeline, but the data dictionaries and validation thresholds were handed to me as a scanned image rather than a text file. 

You need to perform the following steps:

1. **Extract Validation Rules:**
   There is an image located at `/app/cleaning_rules.png`. This image contains numerical thresholds and configuration multipliers needed for our data validation and regression adjustment. Extract these rules (you can use standard OCR tools available in the terminal, like `tesseract`).

2. **Write the C++ Utility:**
   Create a C++ program at `/home/user/cleaner.cpp` and compile it to `/home/user/cleaner`. 
   The program must accept exactly one argument from the command line: a string representing a single row of data in the format: `ID,VALUE,CATEGORY`
   - `ID` is an integer.
   - `VALUE` is a floating-point number.
   - `CATEGORY` is a single uppercase letter.

3. **Validation and Transformation Logic:**
   Based on the rules extracted from the image:
   - Check if `VALUE` is strictly within the inclusive minimum and maximum thresholds. If it is outside this range, your program must print EXACTLY `REJECTED` to standard output and exit with code 0.
   - If `VALUE` is valid, apply the `CLASS_MULTIPLIER` extracted from the image (i.e., multiply `VALUE` by this multiplier).
   - Print the cleaned and adjusted row to standard output in the format: `ID,ADJUSTED_VALUE,CATEGORY` where `ADJUSTED_VALUE` is rounded and formatted to exactly two decimal places (e.g., `42.10`).
   - Print a single newline character at the end of the output.

Make sure your C++ code includes necessary validation to parse the inputs properly and strictly follows the extracted thresholds. Compile your code using `g++` so the executable `/home/user/cleaner` is ready for our automated testing suite, which will fuzz it with thousands of generated rows.