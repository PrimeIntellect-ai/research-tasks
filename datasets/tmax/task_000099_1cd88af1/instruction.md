I need you to help me build a C-based data processing pipeline that reads CSV data, performs feature engineering, and validates model outputs. 

We are using a third-party C library called `libcsv_ext` (version 1.0.0) to help parse the CSV records. The source code for this package is located at `/app/libcsv_ext-1.0.0`. However, the package currently fails to build because of a typo in its `Makefile`. You will need to find the error, fix the `Makefile`, and compile the library (`libcsv_ext.a`).

Once the library is built, write a C program at `/home/user/processor.c` and compile it to `/home/user/processor`. Your program must read a headerless CSV from standard input. Each line of the input will contain exactly four comma-separated fields:
1. `ID` (integer)
2. `Value` (float)
3. `Category` (single character: 'A', 'B', or 'C')
4. `Model_Score` (float)

For each row, your program must apply the following logic:
- **Data Schema Enforcement:** If the `ID` is less than 0, skip the row entirely and produce no output for it.
- **Feature Engineering:** Calculate `Value_squared` by multiplying `Value` by itself.
- **Categorical Encoding:** Map the `Category` character to an integer: 'A' -> 1, 'B' -> 2, 'C' -> 3. Any other character should be mapped to 0.
- **Model Output Validation:** If `Model_Score` is strictly greater than 0.5, the status is "VALID". Otherwise, it is "INVALID".

For every processed row (that isn't skipped), print a comma-separated string to standard output in this exact format:
`ID,Value_squared,Encoded_Category,Validation_Status`

For example, an input line of `10,3.0,B,0.85` should produce the output `10,9.000000,2,VALID` (format floats using `%f`). 

Ensure your program handles EOF correctly and processes all rows. The final executable must be located at `/home/user/processor`. We will test it against a hidden reference implementation with a large number of random CSV inputs to verify its correctness.