You are an AI assistant helping a web developer optimize a critical security feature. We are implementing a custom rate-limiting and token verification backend. The current pure Python implementation is too slow and makes us vulnerable to basic algorithmic denial-of-service attacks. 

Your task is to rewrite the core numerical algorithm in C, compile it into a shared library, bind it back to Python using `ctypes` (FFI), and benchmark the performance to prove the C implementation is faster.

Here are the requirements:

1. **The Algorithm**:
   We use a custom iterative checksum for our security tokens.
   The function takes a `token` (string), a `secret` (string), and an `iterations` (integer) count.
   The pseudocode/Python logic is:
   ```python
   def verify_token(token: str, secret: str, iterations: int) -> int:
       result = 0
       token_len = len(token)
       secret_len = len(secret)
       if token_len == 0 or secret_len == 0:
           return 0
           
       for _ in range(iterations):
           for i in range(token_len):
               s_char = secret[i % secret_len]
               # use ASCII integer values of characters
               val = (ord(token[i]) ^ ord(s_char)) * (i + 1)
               result = (result + val) % 1000003
       return result
   ```

2. **C Implementation**:
   Write this algorithm in C. 
   Save it as `/home/user/app/libverifier.c`.
   The C function signature must be: 
   `long long verify_token(const char* token, const char* secret, int iterations);`
   Compile it into a shared library at `/home/user/app/libverifier.so`.

3. **FFI Binding & Benchmarking**:
   Write a Python script at `/home/user/app/benchmark.py` that:
   - Contains the pure Python `verify_token` implementation.
   - Uses `ctypes` to load `/home/user/app/libverifier.so` and wrap the C `verify_token` function.
   - Tests both implementations with:
     `token = "abc123xyz890"`
     `secret = "super_secure_secret"`
     `iterations = 10000`
   - Asserts that both functions return the exact same integer result.
   - Measures the execution time of both implementations.
   - Writes a log file to `/home/user/app/benchmark_results.log` with exactly this format:
     `Result Match: [True/False] | C_Faster: [True/False] | Python Time: [X.XXXX]s | C Time: [X.XXXX]s`

Create the `/home/user/app/` directory if it does not exist, complete all code and compilation steps, and run your benchmark script so the log file is generated.