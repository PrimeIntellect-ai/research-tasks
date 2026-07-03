You are an open-source maintainer reviewing a broken Pull Request on a Python Web Security project called `waf-emu`. The project evaluates custom WAF (Web Application Firewall) bytecode to detect malicious payloads.

The PR attempts to replace the pure-Python bytecode interpreter with a high-performance Rust shared library, but it is currently failing in CI due to multiple issues:
1. The Rust code has a borrow checker compilation error.
2. The Makefile has a perturbation preventing successful building of the shared library.
3. The Python ABI wrapper (`ctypes`) has incorrect argument/return types causing segfaults or corrupted reads.

The PR code is vendored at `/app/waf-emu`.

Your task is to:
1. Fix the Rust borrow checker error in `/app/waf-emu/rust-core/src/lib.rs`.
2. Fix the `/app/waf-emu/Makefile` so that running `make` correctly builds the release `.so` file and copies it to `/app/waf-emu/py-emu/libwaf_core.so`.
3. Fix the Python bindings in `/app/waf-emu/py-emu/abi.py` to correctly interface with the Rust ABI.
4. Create a standalone execution script at `/home/user/evaluate.py` that accepts exactly two positional CLI arguments: `<bytecode_hex>` and `<payload>`. It must use the fixed `py-emu` package to evaluate the payload and print exactly `BLOCK` or `ALLOW` to standard output.

Ensure your `evaluate.py` strictly outputs only the result string ("BLOCK" or "ALLOW") and no other logging, as it will be heavily fuzzed against a reference oracle to verify correctness.