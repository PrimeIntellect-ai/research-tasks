You are an AI assistant helping a web developer build a mathematical microservice. 

Please create a Go web service that performs numerical integration of polynomials using Simpson's 1/3 Rule. 

Follow these exact specifications:

1. **Project Setup**:
   - Create a directory `/home/user/polycalc`.
   - Initialize a Go module named `polycalc` inside this directory.
   - Install and use `github.com/gorilla/mux` for URL routing.

2. **API Endpoint**:
   - Create a server running on port `8080`.
   - Implement a `GET` endpoint at `/api/v1/integrate/{lower}/{upper}`.
   - `{lower}` and `{upper}` are the limits of integration (float64).
   - The endpoint must accept two URL query parameters:
     - `coeffs`: A comma-separated list of float64 numbers representing the coefficients of a polynomial, ordered from degree 0 upwards. For example, `coeffs=3,2,1` represents $f(x) = 3 + 2x + 1x^2$.
     - `steps`: An integer representing the number of subintervals ($n$) for Simpson's rule.

3. **Mathematical Logic (Simpson's 1/3 Rule)**:
   - Evaluate the integral of the given polynomial from `lower` to `upper` using the provided number of `steps`.
   - Formula: $\int_a^b f(x) dx \approx \frac{h}{3} \left[ f(x_0) + 4 \sum_{i=1,3,5...}^{n-1} f(x_i) + 2 \sum_{i=2,4,6...}^{n-2} f(x_i) + f(x_n) \right]$
   - where $h = \frac{b-a}{steps}$ and $x_i = a + i \cdot h$.

4. **Serialization & Error Handling**:
   - The response must be `Content-Type: application/json`.
   - On success, return HTTP 200 with:
     `{"lower": <float>, "upper": <float>, "steps": <int>, "result": <float>}`
   - If `steps` is not an even integer or is less than 2, return HTTP 400 with:
     `{"error": "steps must be an even integer greater than 0"}`
   - If `coeffs` is invalid or missing, return HTTP 400 with:
     `{"error": "invalid coefficients"}`

5. **Testing & Verification**:
   - Run the server in the background.
   - Write a bash script at `/home/user/test_polycalc.sh` that makes exactly two `curl` requests to your running server:
     - Request 1: Integrate $f(x) = 3 + 2x + x^2$ from 0 to 5, using 100 steps.
     - Request 2: Intentional error to test validation (pass `steps=11`).
   - The script should append the raw JSON responses (each on a new line) to `/home/user/integration_results.log`.
   - Make the bash script executable and execute it so the log file is generated.