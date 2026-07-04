I am a web developer building a backend feature that requires high-performance mathematical calculations. I decided to write the core mathematical logic in Go to utilize its concurrency, but my primary backend service is in Python. 

I have written the Go code in `/home/user/integrate.go`. It calculates Pi using a concurrent Riemann sum over the function `4/(1+x^2)`. It exposes a C-ABI compatible function:
`double CalculatePi(int steps);`

I need you to do the following:
1. Compile the Go code `/home/user/integrate.go` into a C shared library named `/home/user/libintegrate.so`.
2. Write a Python script at `/home/user/test_math.py` that uses the `ctypes` standard library to load `/home/user/libintegrate.so`.
3. In your Python script, configure the correct argument and return types for the `CalculatePi` function.
4. Call `CalculatePi` with `1000000` (one million) steps.
5. Round the result to 6 decimal places.
6. Write the final test result into a JSON file at `/home/user/test_result.json` with the exact following structure:
```json
{
  "module": "libintegrate.so",
  "steps": 1000000,
  "result": <rounded_float_value>
}
```

Ensure the Python script successfully executes and creates the JSON file. You have all the standard tools (Go, Python) available.