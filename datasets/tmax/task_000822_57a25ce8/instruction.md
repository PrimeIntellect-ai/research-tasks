You are a systems programmer debugging a C library linking issue. 
In `/home/user/project`, you have a custom build system and linker emulator written in Python. It compiles a C program against multiple versions of a shared library (`libmathops`). The build system currently fails with an `undefined reference` error because it resolves the wrong version of the library and mishandles symbol resolution states.

Here is the setup of `/home/user/project`:
- `main.c`: The main entry point.
- `libmathops_v1.2.0.c`: An older version of the library.
- `libmathops_v1.10.0-beta.c`: A newer pre-release version of the library containing the symbol `advanced_calculate`.
- `libmathops_v1.10.0.c`: The latest stable version of the library containing the stable `advanced_calculate`.
- `deps.symmap`: A custom structured file describing the symbols exported by each library version.
- `semver_utils.py`: Contains a buggy semantic version comparison function `compare_versions(v1, v2)`. It currently uses naive string comparison, which incorrectly evaluates `1.10.0` as older than `1.2.0`, and mishandles pre-release tags (e.g., `1.10.0-beta` should be older than `1.10.0`).
- `sym_emulator.py`: Contains a state machine (`SymbolResolver`) that parses `deps.symmap` and emulates linker symbol resolution. It tracks states (`UNRESOLVED`, `WEAK_RESOLVED`, `STRONG_RESOLVED`). There is a bug where it fails to transition from `WEAK_RESOLVED` to `STRONG_RESOLVED` when a strong symbol is encountered.
- `build.py`: The entry point that uses `semver_utils.py` to find the highest stable version of the library, uses `sym_emulator.py` to verify symbol resolution, and then compiles the C code.

Your tasks are:
1. Fix the `compare_versions(v1, v2)` function in `semver_utils.py`. It must return `-1` if `v1 < v2`, `1` if `v1 > v2`, and `0` if equal, correctly handling major.minor.patch formats and pre-release tags (e.g. `-beta`, `-alpha`). Pre-release tags have lower precedence than the normal version (e.g., `1.10.0-beta` < `1.10.0`).
2. Write a property-based test in `/home/user/project/test_semver.py` using the Python `hypothesis` library. You must test the property that for any randomly generated semver strings `v1` and `v2`, `compare_versions(v1, v2)` returns the opposite sign of `compare_versions(v2, v1)` (anti-symmetry). You must install `hypothesis` using `pip`.
3. Fix the state machine logic in `sym_emulator.py` so that a `WEAK_RESOLVED` symbol correctly upgrades to `STRONG_RESOLVED` when a strong definition is found in the `.symmap`.
4. Run `python build.py`. If you fixed the Python files correctly, it will successfully compile the correct library (`libmathops_v1.10.0.so`) and link it to `app`.
5. Run the compiled application and redirect its output to `/home/user/project/success.log`:
   `LD_LIBRARY_PATH=. ./app > /home/user/project/success.log`

Ensure `success.log` contains the final output of the C application.