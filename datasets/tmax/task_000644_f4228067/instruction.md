You are a web developer working on a backend feature for a specialized mathematical API. The project is a multi-file Python service that decodes an incoming query, parses it into a mathematical representation, and uses a numerical algorithm to compute the root of a polynomial.

Currently, the project is broken. Several files contain bugs ranging from incorrect character decoding and flawed state machine logic to a mathematically incorrect implementation of Newton's method. 

Your task is to debug, fix, and correctly configure the application in `/home/user/math_api`, then process a specific encoded query and save the result.

### System Specifications

**1. Encoding Rules (`decoder.py`)**
Incoming queries are passed as hex strings. The decoding process must:
- Convert the hex string into a byte array.
- XOR each byte with the key `0x42`.
- Decode the resulting bytes as an ASCII string.
*Current Bug:* The existing `decoder.py` incorrectly XORs the hex characters instead of the bytes, and fails to handle ASCII conversion properly.

**2. Parser Rules (`parser.py`)**
The decoded ASCII string is a custom command format: `P <c0> <c1> ... <cn> | G <guess>`
- `P` defines a polynomial $P(x) = c_0 + c_1 x + c_2 x^2 + \dots + c_n x^n$. Coefficients are space-separated floats.
- `|` is the delimiter between the polynomial definition and the guess.
- `G` defines the initial guess for the root-finding algorithm as a float.
*Current Bug:* The state machine parser in `parser.py` fails to parse negative coefficients correctly (it drops the negative sign or transitions to an error state) and struggles with multiple spaces.

**3. Numerical Algorithm (`solver.py`)**
The system uses Newton's method to find a root of the parsed polynomial:
$$x_{n+1} = x_n - \frac{P(x_n)}{P'(x_n)}$$
- Tolerance: Stop when $|P(x_n)| < 1e-7$.
- Maximum iterations: 100.
*Current Bug:* The implementation of the derivative evaluation $P'(x)$ in `solver.py` has an off-by-one indexing error, causing it to compute the wrong derivative values and fail to converge.

### Your Objectives

1. Review and fix the bugs in `/home/user/math_api/decoder.py`.
2. Review and fix the state machine logic in `/home/user/math_api/parser.py`.
3. Fix the derivative and Newton's method logic in `/home/user/math_api/solver.py`.
4. Install any necessary dependencies to run a Python project (e.g., `pytest` if you want to write your own tests).
5. Once the code is fixed, use the provided `main.py` script to process the following hex query:
   `12626e276c70227222726c7122726c7322727c622562732c22`
6. Output the final computed root (rounded to 6 decimal places) to a file exactly at `/home/user/result.txt`. The file should contain *only* the float value, e.g., `1.414214`.

All project files are located in `/home/user/math_api`. You must fix the code in place.