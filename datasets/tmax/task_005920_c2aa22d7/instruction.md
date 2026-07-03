**Ticket #8831: Billing Processor Crashing and Losing Precision**

**Role:** IT Support Technician (Tier 3)

**Issue Description:**
The billing department reported that our legacy C++ batch processing utility, located at `/home/user/ticket_8831/processor.cpp`, is generating incorrect totals for large datasets and frequently crashes or returns garbage data on edge cases. 

Upon initial inspection, the container logs (simulated here via standard execution) show sporadic segmentation faults or incorrect accumulations. We suspect there are boundary condition issues (off-by-one errors) and precision loss during the aggregation of floating-point financial data.

**Your Tasks:**
1. **Debug and Fix the Code:**
   - Locate and fix the boundary condition / off-by-one error in the main loop of `/home/user/ticket_8831/processor.cpp`.
   - Upgrade the internal accumulation variables and data structures to track precision correctly (use `double` instead of `float` to prevent precision loss over large datasets).
   - Add at least two `assert()` statements in the C++ code to validate intermediate states (e.g., ensuring the vector is not empty before processing, and validating index bounds).

2. **Regression Test Construction:**
   - Create a regression test script at `/home/user/ticket_8831/test.sh`.
   - The script must compile `processor.cpp` into an executable named `processor`.
   - The script must run the compiled executable against `/home/user/ticket_8831/data.txt`.
   - The script should return exit code `0` if successful. Ensure you make this script executable (`chmod +x`).

3. **Verification Output:**
   - Execute your fixed program against `/home/user/ticket_8831/data.txt`.
   - Save the exact standard output (the calculated sum, formatted to 6 decimal places) into a log file at `/home/user/ticket_8831/resolution.log`.

**Environment:**
- The source file `processor.cpp` and the dataset `data.txt` have been provided in `/home/user/ticket_8831/`.
- You may use `g++` to compile the code.

Please diagnose, fix, and verify the solution. The automated system will check `resolution.log` for the exact corrected total and execute `test.sh` to ensure the regression test passes.