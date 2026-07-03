You are the on-call engineer and just received a 3 AM page. The backend calculation service is experiencing a severe outage. Instances of the service are pegging CPU at 100% and timing out when processing large inputs, whereas they used to return instantly.

You have been granted access to the service's repository located at `/home/user/calc_service`. 

Here is what we know:
1. **The Outage:** The C program `calc.c` computes a sequence. It works fine for small inputs (e.g., `./calc 10`) but goes into an infinite loop for large inputs (e.g., `./calc 100000000`). Initial reports suggest the loop termination fails because a variable becomes `NaN` or `Inf` due to a numerical instability (catastrophic cancellation) in the formula `sqrt(x^2 + 1) - x`.
2. **The Secret:** Yesterday, a junior developer accidentally committed a production API key to `calc.c` and later removed it in a panic commit. The security team needs that key immediately to rotate it.

Your tasks:
1. **Recover the API Key:** Dig through the git history in `/home/user/calc_service` and find the leaked API key. Save the exact key string to `/home/user/api_key.txt`.
2. **Fix the Calculation:** Modify `/home/user/calc_service/calc.c` to resolve both the numerical instability and the infinite loop. You must rewrite the mathematically equivalent but stable expression for `sqrt(x^2 + 1) - x` to prevent catastrophic cancellation, and ensure the loop terminates gracefully (e.g., handling precision limits or `NaN` explicitly if needed, though fixing the math should prevent `NaN`). The program must compile with standard `gcc -lm calc.c -o calc`.
3. **Write a Regression Test:** Create an executable bash script at `/home/user/calc_service/test.sh` that compiles `calc.c` and runs it with the input `100000000`. The script must enforce a 2-second timeout on the execution (using the `timeout` command) to ensure it doesn't spin infinitely. It should exit with code 0 if the C program succeeds within the timeout and outputs a valid number, and exit with code 1 otherwise.

Fix the code, recover the key, and write the test script.