I am a researcher organizing a large collection of sensor datasets. A while ago, I wrote a C program to preprocess these datasets. The program takes a stream of raw 32-bit signed integers (representing raw sensor readings) from standard input and outputs 32-bit floats to standard output. 

I lost the source code for this preprocessor, but I still have the compiled, stripped binary located at `/app/cleaner_oracle`. 

I need you to recreate the C source code for this preprocessor and compile it. 
Here is what I remember about the preprocessing logic:
1. It reads `int32_t` values from standard input until EOF.
2. It handles "missing" sensor data. There is a specific integer value that indicates a missing reading, which gets converted to an IEEE 754 NaN (Not a Number) in the float output.
3. Valid readings are converted to floats using a simple linear scaling factor (a multiplier).
4. The output is written to standard output as raw binary `float` (32-bit) values.

Please reverse-engineer the `/app/cleaner_oracle` binary to determine the exact missing value trigger, the NaN bit-pattern used, and the scaling factor. 

Write your C code to `/home/user/cleaner.c` and compile it to `/home/user/cleaner`. Your compiled program must be bit-exact equivalent to the oracle binary for any arbitrary sequence of input integers. 

Your program should use standard library functions. Make sure it can handle inputs of any length.