You are a data engineer tasked with fixing and integrating an ETL pipeline. We have a microservice architecture consisting of a configuration server (a Python Flask app) and a caching layer (Redis). 

Currently, our pipeline includes a C program that normalizes a stream of floating-point numbers. However, the existing implementation suffers from a critical data leakage bug: it reads the entire dataset into memory and computes the mean and standard deviation over all data (future and past) before normalizing, which leaks test data statistics into the training phase.

Your task is to:
1. Reconfigure and start the services. 
   - A Redis server must be started on port 6379.
   - A Flask app located at `/app/config_service.py` must be started on port 5000.
2. Write a new C program at `/home/user/normalize_stream.c` and compile it to `/home/user/normalize_stream`.
3. The C program must read configuration at startup:
   - It should perform an HTTP GET request to `http://127.0.0.1:5000/window` to retrieve the rolling window size (an integer).
   - It should connect to Redis on `127.0.0.1:6379` and GET the key `fallback_mean` (a float).
4. The program will read a sequence of floating-point numbers from standard input (one per line).
5. For each number, it must compute its normalized value `(x - mean) / std` and print it to standard output, formatted to exactly 4 decimal places (`%.4f`), one per line.
   - The `mean` and `std` (sample standard deviation) must be computed ONLY using up to the last `W` numbers previously seen in the stream, where `W` is the window size fetched from the Flask app. 
   - The current number `x` being processed MUST NOT be included in the mean/std calculation.
   - If 0 numbers have been seen (i.e., for the very first number), use the `fallback_mean` from Redis as the mean, and `1.0` as the std.
   - If only 1 number has been seen, the sample std is undefined. In this case, or anytime the sample std is exactly `0.0`, use `1.0` as the std.

Requirements:
- Do not use future data (no data leakage).
- Standard deviation must be the sample standard deviation (divide by N-1).
- Use `libcurl` for the HTTP request and `hiredis` for the Redis connection. You may need to install these packages.
- Compile your code to `/home/user/normalize_stream` so it can be verified.

The verification process will send random streams of numbers to your program's stdin and compare its bit-exact stdout against our reference oracle.