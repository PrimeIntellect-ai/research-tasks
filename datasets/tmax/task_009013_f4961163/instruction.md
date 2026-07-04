Wake up, you're on call and it's 3 AM. Our nightly financial risk calculation service just crashed out of memory and the emergency patch is failing to compile. The automated system captured a partial core dump before the container died. 

Your objectives to resolve the incident:

1. **Extract the Faulting ID**: Analyze the raw memory dump located at `/home/user/risk_engine/crash.dump`. The crash was triggered by a specific transaction. Extract the transaction ID (which follows the format `TXID-[5 digits]-[UPPERCASE_WORD]`, e.g., `TXID-12345-ALPHA`). Save *only* this exact transaction ID string to a new file at `/home/user/extracted_tx.txt`.

2. **Resolve Compilation Errors**: Our junior engineer attempted an emergency patch, but now the project won't build. Navigate to `/home/user/risk_engine`. If you run `cargo build`, you will see compiler errors related to mismatched types. This is caused by a dependency conflict between local crates in the workspace (`common_types` version mismatch between `risk_engine` and the `math_utils` library). Resolve the dependency conflict by modifying the `Cargo.toml` files so the project compiles successfully. Do not alter the function signatures in the Rust source code to fix this; fix the dependencies.

3. **Repair Floating-Point Precision**: The root cause of the crash was an infinite loop triggered by a floating-point precision error in `/home/user/risk_engine/src/main.rs`. The `calculate_risk_score` function loses precision during its iterative compounding calculation because it uses `f32`, failing the safety assertion. Repair the function to use standard `f64` precision so that it accurately computes the risk score and passes its embedded tests (`cargo test`).

4. **Verify and Execute**: Once the compilation and algorithmic issues are fixed, run the compiled binary, passing the extracted transaction ID as the single argument:
   `cargo run -- <EXTRACTED_TX_ID>`
   
   The program will output a final calculated risk score. Save this exact numeric score to `/home/user/final_score.txt`.