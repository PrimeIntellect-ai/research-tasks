You are an IT support technician resolving Ticket #4492.

**Ticket Description:**
The finance team uses an internal Python script to query users with specific account balances from our daily transaction CSV. However, they report that certain queries are returning empty results, even when there are clearly transactions that sum up to the exact target amount. 

For example, when they run:
`python3 /home/user/billing_query.py --target 15.30`
It returns no users, despite "alice" having transactions of 15.10 and 0.20, and "bob" having 10.00 and 5.30.

Your objective is to investigate and resolve this issue. You must apply your skills in debugging query results, floating-point precision repair, minimal reproducible example (MRE) creation, and fuzz testing.

**Tasks:**
1. **Fix the Application**: Modify `/home/user/billing_query.py` to fix the precision error causing the query failure. You must replace standard float operations with exact decimal arithmetic (e.g., using Python's `decimal` module) so that the sums exactly match string representations of the target amounts.
2. **Generate the Correct Report**: Run your fixed script with `--target 15.30` and redirect the standard output to `/home/user/ticket_4492_output.txt`. 
3. **Create an MRE**: Create a script at `/home/user/mre.py` that serves as a minimal reproducible example of the original bug. The script should assign `15.10` and `0.20` to standard Python `float` variables, add them, compare them to the float value of `15.30`, and print the boolean result of that equality check to standard output.
4. **Fuzz Test the Fix**: Create a script at `/home/user/fuzz_test.py` that acts as a fuzzer to prove standard floats fail while your fix works. It should:
   - Loop 1000 times.
   - In each iteration, generate two random 2-decimal-place strings (e.g., "12.34").
   - Add them using `float` and add them using `decimal.Decimal`.
   - Keep a count of how many times the `float` addition exactly equals the float of the expected string sum, versus how many times `decimal.Decimal` equals the `Decimal` of the expected string sum.
   - Write the string "FUZZ_OK" to `/home/user/fuzz.log` upon completion if the `Decimal` approach achieves 1000/1000 matches.

Provide the commands to achieve this state. Ensure all requested files exist at the exact paths specified.