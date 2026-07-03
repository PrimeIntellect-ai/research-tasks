You are a support engineer investigating a critical data processing escalation. The customer provided a diagnostic bundle located at `/home/user/support_bundle`. The system consists of a Python data processing script that relies on a C-extension for performance, but it is currently failing to build and falling back to a buggy Python implementation that introduces precision loss. Furthermore, the system logs are scattered across three services with different timestamp formats, making it hard to find when the precision loss first triggered an error.

Your objectives:

1. **Fix the Compiler/Linker Error**:
   The customer's custom C-extension is located in `/home/user/support_bundle/ext`. Running `python3 setup.py build_ext --inplace` fails due to an unresolved symbol error (a linker issue). Diagnose the missing library, modify `setup.py` to include the correct linker flag, and successfully build the extension in place.
   Save a unified diff of your changes to `setup.py` in `/home/user/support_bundle/build_fix.patch`.

2. **Fix the Precision Loss**:
   The script `/home/user/support_bundle/process_data.py` reads values from `data.csv` and calculates a total sum. Because the C-extension was broken, it fell back to a naive Python loop that suffers from catastrophic cancellation (floating-point precision loss) when handling large and small numbers together.
   Fix the Python fallback logic in `process_data.py` so that it computes the exact, mathematically correct sum without precision loss (hint: standard library modules can help).
   Run the script and save the correct total sum to `/home/user/support_bundle/corrected_sum.txt`.

3. **Reconstruct the Log Timeline**:
   The `logs` directory contains `service_A.log`, `service_B.log`, and `service_C.log`. 
   Parse all three logs, normalize their timestamps to standard ISO8601 format (e.g., `YYYY-MM-DDTHH:MM:SSZ`), and sort them chronologically. Find the exact Transaction ID (e.g., `TXN-...`) where a precision mismatch error is first reported.

4. **Generate Diagnostic Report**:
   Create a JSON file at `/home/user/diagnostic_report.json` with the following structure:
   ```json
   {
     "missing_linker_library": "<the string you added to the libraries list in setup.py, e.g., 'z'>",
     "corrected_total_sum": "<the exact sum as a string>",
     "first_failing_transaction_id": "<the TXN id found in the logs>"
   }
   ```