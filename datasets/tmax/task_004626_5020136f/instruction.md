You have been assigned to investigate a regression in a Go-based system utility called `metrics-parser`. 

The repository is located at `/home/user/metrics-parser`. 
The `main` branch currently fails its test suite (`go test ./...`) with a panic. This regression was introduced somewhere between the known-good tag `v1.0.0` and the current `HEAD` (`v1.1.0`), spanning about a dozen commits.

Your objectives are:
1. **Bisect the regression**: Find the exact commit that introduced the bug. The bug causes a panic due to an off-by-one boundary condition and format parsing edge-case when processing malformed or trailing data.
2. **Record the bad commit**: Write the full 40-character Git SHA of the commit that introduced the bug into `/home/user/bad_commit.txt`.
3. **Fix the bug**: Checkout the `main` branch (at `v1.1.0`), and fix the code in `parser.go` so that it handles the boundary condition correctly and the test suite passes (`go test ./...` returns exit code 0). Do not modify the test file itself.

Constraints:
* Do not change the test data or the test file `parser_test.go`.
* You must resolve the panic by safely handling the parsing edge-case in `parser.go`.
* Ensure you are on the `main` branch when applying your final fix.