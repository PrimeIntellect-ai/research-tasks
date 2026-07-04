Wake up! It's 3:00 AM and you've just been paged. The critical Tier-3 Billing Aggregation Service has crashed in production, preventing enterprise customers from processing payments. 

The DevOps team managed to capture a raw memory dump of the crashed process before restarting it, and they have placed it at `/home/user/crash.dmp`. You have access to the service's source code in `/home/user/billing-service`.

Your mission is to diagnose the crash, fix the underlying logic error, and provide an incident resolution report.

Here are your specific objectives:

1. **Memory Dump Analysis**: Analyze the binary dump file located at `/home/user/crash.dmp`. Somewhere in the heap memory strings, the service logged the exact transaction ID right before it panicked. Extract the transaction ID, which is prefixed with `FATAL_ERROR_FOR_TRACE_ID: `.

2. **Formula Implementation Correction**: 
   The service crashed due to an arithmetic panic (integer underflow) in the billing calculation.
   Review and fix the logic in `/home/user/billing-service/src/calculator.rs`. The function `calculate_cost(base: u64, multiplier: u64, discount: u64) -> u64` is faulty. It currently attempts to multiply the base by the multiplier and then subtract the discount. 
   You must fix it so that:
   - All arithmetic operations use Rust's saturating arithmetic (e.g., if the discount is greater than the subtotal, the final cost should be `0`, not panic).

3. **Intermediate State Tracing**:
   To help our QA team ensure this doesn't happen again, modify the `calculate_cost` function to write its intermediate state to `/home/user/trace_output.log`.
   Specifically, *before* applying the discount, append a line to `/home/user/trace_output.log` in the exact format:
   `[<EXTRACTED_TRACE_ID>] Intermediate Subtotal: <SUBTOTAL>`
   (Replace `<EXTRACTED_TRACE_ID>` with the actual ID you found in step 1, and `<SUBTOTAL>` with the saturating product of base and multiplier).

4. **Incident Resolution Report**:
   Create a file at `/home/user/resolution.txt` containing exactly two lines:
   Line 1: The extracted trace ID in the format: `TRACE_ID: <ID>`
   Line 2: The calculated final cost for a test case where base=1500, multiplier=3, and discount=5000, in the format: `FIXED_TEST_COST: <COST>`

*Note: You may use standard CLI tools (strings, grep, etc.) to analyze the dump. You must write the Rust code fixes and ensure the project builds correctly via `cargo build`.*