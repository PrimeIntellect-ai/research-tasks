You are a mobile build engineer tasked with maintaining our automated pipeline. We recently introduced a pre-build validation step that analyzes minimal ARM assembly artifacts to determine which mobile hardware targets are compatible before we attempt a full monolithic build and linking phase.

You need to write a Python script that parses assembly-level constraints and generates a pytest fixture containing the satisfied hardware targets. 

Here are the details:
1. You have an assembly trace file located at `/home/user/asm_trace.s`. This file contains standard ARM assembly, but our static analysis tool has injected specific comment directives indicating hardware and linking constraints.
   - Directives format: `; REQUIRE <KEY> <OP> <VALUE>` or `; CONFLICT <KEY> <VALUE>`
   - Example 1: `; REQUIRE MEM >= 2048` (Target must have >= 2048 MB memory)
   - Example 2: `; REQUIRE CPU_EXT NEON` (Target must have 'NEON' in its CPU_EXT list)
   - Example 3: `; CONFLICT CPU_EXT VFPV3` (Target must NOT have 'VFPV3' in its CPU_EXT list)

2. You have a JSON database of all available build targets at `/home/user/build_targets.json`. Each entry has a `name` (string), `MEM` (integer), and `CPU_EXT` (list of strings).

3. Write a Python script at `/home/user/generate_fixture.py`. The script must:
   - Read `/home/user/asm_trace.s` and parse all `REQUIRE` and `CONFLICT` constraints.
   - Read `/home/user/build_targets.json`.
   - Implement constraint satisfaction to filter out any targets that do not meet ALL requirements or that trigger ANY conflicts.
   - Generate a valid pytest fixture file at `/home/user/test_fixture.py`. 

The output file `/home/user/test_fixture.py` MUST have exactly this format:
```python
import pytest

@pytest.fixture
def valid_targets():
    return [
        "target_name_1",
        "target_name_2"
    ]
```
(Sort the target names alphabetically).

Run your script to produce `/home/user/test_fixture.py` so it can be verified.