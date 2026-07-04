You have just inherited an unfamiliar Go codebase located in `/home/user/physics`. The previous developer was building a mathematical utility for calculating the 1D Center of Mass, but they left the project in a broken state and abruptly quit.

Before leaving, they sent a message:
*"I accidentally deleted the `vectors.json` file containing the golden test cases. However, I know the `test_daemon.py` process is still running in the background and holds an open file descriptor to it."*

Your objectives are to fix the repository and stabilize the code:

1. **Deleted File Recovery:** 
   Locate the background process holding the deleted `vectors.json` file open. Recover the contents of the file and save it back to `/home/user/physics/vectors.json`.

2. **Formula Implementation Correction:**
   The `CalculateCenterOfMass` function in `/home/user/physics/calc.go` has a logic bug in its mathematical formula. Read the expected inputs and outputs from the recovered `vectors.json` to deduce the correct behavior and fix the formula implementation in `calc.go`. 

3. **Fuzz Testing & Robustness:**
   The function currently panics under certain edge cases. 
   - Write a Go fuzz test named `FuzzCalculateCenterOfMass` inside `/home/user/physics/calc_test.go`. Ensure it fuzzes the function with various slices of `float64` for positions and weights.
   - Use the fuzzer to discover the panic condition.
   - Modify the signature of the function to return an error: `func CalculateCenterOfMass(positions []float64, weights []float64) (float64, error)`.
   - Fix the panic by returning `0.0` and `errors.New("zero weight sum")` when that specific condition is met, and update the rest of the code accordingly.

4. **Verification:**
   Run your tests and fuzzing (e.g., `go test` and `go test -fuzz=FuzzCalculateCenterOfMass -fuzztime=3s`). Save the standard output of a successful test execution (showing both unit tests and fuzz tests passing) to `/home/user/physics/test_results.log`.