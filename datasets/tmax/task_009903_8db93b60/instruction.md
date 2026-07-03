You are a web developer building a backend feature for an educational math game. You need to implement a standalone C++ tool that simulates a web endpoint. This tool will parse a URL, interpret a dynamic mathematical equation, and solve a basic constraint satisfaction problem to find the correct variables.

Write a C++ program at `/home/user/router_solver.cpp` that fulfills these requirements:

1. **Input:** The program takes exactly one command-line argument: a URL string. 
   Example: `/route/calc?eq=x*y+y&res=27&range=1,10`

2. **URL Routing and Parameter Parsing:**
   - The program must verify that the URL path is exactly `/route/calc`. If it is any other path, print `{"error": "not found"}` to standard output and exit with code 1.
   - Parse the query string into three parameters:
     - `eq`: A mathematical expression string.
     - `res`: An integer representing the target result.
     - `range`: A string in the format `min,max` (two integers).

3. **Expression Interpreter:**
   - Implement a small interpreter to evaluate the `eq` string for given values of `x` and `y`.
   - The expression will only contain the variables `x` and `y`, and the operators `+` and `*`. 
   - Standard mathematical precedence applies (evaluate `*` before `+`). There will be no parentheses.

4. **Constraint Satisfaction:**
   - Find integer values for `x` and `y` such that the evaluated expression equals the target `res`.
   - Constraints on the search space: `min <= x <= y <= max`.
   - Iterate to find the solution. Search `x` from `min` to `max`, and for each `x`, search `y` from `x` to `max`. Stop and return the *first* pair that satisfies the equation.

5. **Output Format:**
   - Print the solution to standard output as a JSON object: `{"x": X, "y": Y}`.
   - If no solution exists within the range, print `{"error": "no solution"}` to standard output.

Compile your program using:
`g++ -std=c++17 -O2 -o /home/user/router_solver /home/user/router_solver.cpp`

Once compiled, write a bash script at `/home/user/test.sh` that runs your compiled program with the exact argument:
`/route/calc?eq=x*x+y*y&res=25&range=1,10`
and redirects the standard output to `/home/user/output.json`. 

Ensure `/home/user/test.sh` is executable and run it to produce the `output.json` file.