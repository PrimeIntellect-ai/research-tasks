You are tasked with developing a Python utility that resolves and links dependencies based on semantic version requirements, along with a property-based test suite.

You are provided a project directory at `/home/user/project` and a local library cache at `/home/user/libs`. 

1. Write a Python script at `/home/user/project/linker.py`. The script must:
   - Implement a custom data structure called `SemVer` to parse and compare semantic versions (e.g., `MAJOR.MINOR.PATCH`). It must support standard comparison operators (`<`, `<=`, `==`, `>=`, `>`).
   - Read `/home/user/project/link_config.txt`, which contains build system linking dependencies. Each line has the format `<library_name> <version_requirements>` (e.g., `libA >=1.1.0,<2.0.0`).
   - Scan the `/home/user/libs/` directory. For each library requested, find all matching available versions in the format `<library_name>-<MAJOR.MINOR.PATCH>`.
   - Resolve the dependency by selecting the *highest* available version that satisfies the requirements.
   - Automatically configure the build environment by creating a symbolic link in `/home/user/project/build/` for each resolved library. The symlink should be named `<library_name>` and point to the chosen version directory in `/home/user/libs/`. If the `build` directory doesn't exist, create it.

2. Write a property-based testing file at `/home/user/project/test_linker.py` using the `hypothesis` framework.
   - It must import the `SemVer` class from `linker.py`.
   - Implement at least one test using `@given` that verifies the *transitive property* of your `SemVer` comparisons (i.e., for any three valid versions a, b, c: if a < b and b < c, then a < c).
   - Ensure the tests pass when run with `pytest`.

Your solution should be self-contained and assume the `hypothesis` and `pytest` packages are installed. Execute your `linker.py` script so that the `build` folder and its symlinks are generated.