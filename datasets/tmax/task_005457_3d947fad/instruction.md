You are a data scientist responsible for building a reproducible data transformation pipeline for tabular data. A domain expert has provided a specific feature engineering formula, but unfortunately, it was only provided as an image located at `/app/formula.png`.

Your task is to:
1. Extract the mathematical formula from the image `/app/formula.png`. You can use `tesseract` or any other available CLI tool to read the text. The image contains a single line of text defining how to compute a `result` from three variables `a`, `b`, and `c`.
2. Write a C++ program `transform.cpp` that implements this formula for tabular data transformation. 
3. The program should read from standard input until EOF. Each line of input will contain exactly three space-separated integers representing `a`, `b`, and `c`.
4. For each line, compute the transformation according to the extracted formula and print the integer result on a new line to standard output.
5. Compile your C++ code into an executable named `/home/user/transform`. 

This executable will be heavily benchmarked for inference performance, and its behavior will be rigorously checked against an automated reference implementation using random tabular inputs.