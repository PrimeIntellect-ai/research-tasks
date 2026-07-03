You are a mobile build engineer responsible for maintaining CI/CD pipelines. We have a legacy build configuration format called BCD (Build Constraint Definition) that defines parameters for our mobile app's automated test suite. The bash scripts that previously parsed this are failing due to new mathematical requirements.

Your task is to write a custom Rust CLI tool that acts as an interpreter for this BCD configuration, validates build rate limits, and generates a JSON test fixture for our mobile UI testing framework.

**File Location:**
The configuration file is located at `/home/user/build_config.bcd` (you do not need to create this file; assume it already exists).

**BCD Format Specification:**
The file consists of key-value pairs separated by ` = `.
Keys are alphanumeric. Values are either:
1. A string starting with `/` (e.g., `/api/v1/sync`).
2. An integer.
3. A Reverse Polish Notation (RPN) mathematical expression containing previously defined keys, integers, and the operators `+` and `*`.

Example:
```
BaseX = 1000
BaseY = 2000
Density = 3
MaxAssetSize = BaseX BaseY * Density *
ApiEndpoint = /api/v1/sync
RateLimit = 50
MaxRequests = RateLimit 2 * 10 +
```

**Your Objective:**
1. Create a new Rust project at `/home/user/bcd_eval`.
2. Write an interpreter in Rust that reads `/home/user/build_config.bcd`.
3. Evaluate all variables. Your RPN evaluator must correctly compute the mathematical expressions.
4. **Validation / Rate Limiting:** The interpreter must check the evaluated value of the `RateLimit` variable. If `RateLimit` is greater than `60`, your Rust program must immediately print an error to standard error and exit with status code `1`.
5. **Mock / Test Fixture Setup:** If validation passes, the program must output a valid JSON file to `/home/user/mobile_mock.json`. This JSON object must contain all the keys and their evaluated values (numbers as JSON integers, strings as JSON strings).

**Requirements:**
- The resulting JSON must be written exactly to `/home/user/mobile_mock.json`.
- The Rust project should be runnable via `cargo run --manifest-path /home/user/bcd_eval/Cargo.toml`.
- You may use external crates (like `serde_json`) by adding them to your `Cargo.toml`.
- Do not make assumptions about the variable names other than `RateLimit` having special validation logic.