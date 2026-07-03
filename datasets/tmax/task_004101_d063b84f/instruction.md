You are an operations engineer triaging a critical incident. Our data processing pipeline has started producing inaccurate results after a recent update to our custom data transformation library.

We have a vendored copy of the library located at `/app/libdatatransform-1.0`. The library is written in C and is responsible for applying a multi-stage numerical filter to our sensor data.

Users have reported that the output data suffers from significant precision loss, leading to downstream failures. 
Your tasks are to:
1. Analyze the C source code in `/app/libdatatransform-1.0` to track down the root cause of the precision loss. You may need to use delta debugging on the input data or track the transformation diffs to isolate the problematic function.
2. Fix the source code to restore full double-precision accuracy.
3. Recompile the library and its CLI tool using the provided `Makefile`.
4. Run the fixed tool on the input dataset located at `/home/user/sensor_input.bin`.
5. Save the processed output to exactly `/home/user/sensor_output.bin`.

The input file `/home/user/sensor_input.bin` contains exactly 10,000 `double` (64-bit float) values.
The output file `/home/user/sensor_output.bin` must also contain exactly 10,000 `double` values.

Do not use any external libraries other than standard C libraries. The correctness of your fix will be evaluated by calculating the Mean Absolute Error (MAE) between your output and a known-good reference output.