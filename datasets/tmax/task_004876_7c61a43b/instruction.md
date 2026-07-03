I am a researcher organizing large tabular datasets of 3D spatial measurements. As part of our data pipeline, we have a legacy binary utility that performs critical mathematical feature engineering on our coordinate data. Unfortunately, the source code was lost, and all we have is a stripped binary located at `/app/spatial_transformer`.

I need you to recreate this reproducible data transformation pipeline in clean C++.

Here is what we know about the legacy binary:
- It processes standard input (stdin) line by line.
- Each input line is a comma-separated string containing an integer ID and three floating-point coordinates: `id,x,y,z`.
- For each input line, it outputs a single comma-separated line to standard output (stdout) containing the original `id` followed by 6 engineered mathematical features: `id,f1,f2,f3,f4,f5,f6`.
- The engineered features are basic mathematical aggregations, combinations, and transformations of `x`, `y`, and `z` (think distances, interaction terms, basis functions, or sums).
- All floating-point outputs are printed to exactly 6 decimal places.

Your tasks:
1. Interrogate the `/app/spatial_transformer` binary by feeding it various mathematical test inputs to deduce the exact formulas for `f1` through `f6`. You might need to use regression or statistical modeling to discover the patterns.
2. Write a clean C++ implementation of this transformation in `/home/user/recreated_pipeline.cpp`.
3. Compile your code to produce an executable at `/home/user/spatial_transformer_recreated`. 
4. Ensure your C++ program exactly matches the output format of the legacy binary for any valid input line. It should process stdin to stdout indefinitely until EOF.

The automated verification system will randomly generate thousands of inputs to fuzz your executable and compare its output bit-for-bit against the legacy binary. Make sure your mathematical operations are precisely equivalent and that your precision formatting matches.