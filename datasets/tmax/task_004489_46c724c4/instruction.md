You are tasked with finding and fixing a regression in a Go data processing application.

The application is located in `/home/user/app`. It reads a JSON file of inventory items, calculates the final price after discounts, and outputs a new JSON file. 

At the Git tag `v1.0`, the application worked perfectly. However, over the course of the subsequent 200 commits up to `HEAD`, a regression was introduced that causes the final total calculations to be incorrect. 

Your objectives are:
1. **Bisect the repository** to find the exact commit hash that introduced the bug.
2. Write **ONLY** the full Git commit hash of the bad commit to `/home/user/bug_commit.txt`.
3. **Fix the bug** in `processor.go` at the current `HEAD`.
4. Run your fixed code against `data.json` and save the output to `/home/user/fixed_output.json`.
   Use the command: `go run processor.go data.json /home/user/fixed_output.json`

You should use your debugging and shell scripting skills (e.g., `git bisect`, writing a quick test script to evaluate commit correctness, and examining code diffs) to find and resolve the issue. 

Constraints:
- The input data file `data.json` is provided in the repository.
- A correct calculation for an item is `Total = Quantity * Price * (1.0 - Discount)`.
- Do not modify `data.json`.
- Provide the final output in exactly the same JSON format as the original application intended.