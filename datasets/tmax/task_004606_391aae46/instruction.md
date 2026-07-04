You are a data analyst working on a high-throughput CSV processing pipeline. 

Your manager has given you an image containing the specific business logic for a new data filter and aggregation tool. The specification image is located at `/app/spec.png`. 

Your task is to:
1. Extract the text/rules from the image `/app/spec.png` (you can use `tesseract` or any other available OCR tool).
2. Write a C++ program at `/home/user/filter_aggregate.cpp` that implements exactly the logic described in the image.
3. The program must read a headless CSV from standard input (stdin) and print the results to standard output (stdout).
4. Compile your program to an executable located exactly at `/home/user/filter_aggregate`. 

The system provides a reference oracle binary at `/app/oracle_bin`. Your compiled program must produce **bit-exact identical output** to this oracle for any valid CSV input matching the domain described in the image. 

Make sure your C++ code handles standard edge cases (e.g., empty input, missing values handled as per standard parsing) and uses precision formatting that matches standard C++ float/double default string casting, as the oracle does the same.

Compile your code using:
`g++ -O3 -std=c++17 /home/user/filter_aggregate.cpp -o /home/user/filter_aggregate`