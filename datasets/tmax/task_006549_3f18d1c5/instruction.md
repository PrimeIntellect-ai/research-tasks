You are a developer organizing a set of project files and tracking their release versions. You have been provided a text file at `/home/user/versions.txt` containing a list of version tags, one per line.

Your task is to write a C++ program at `/home/user/sorter.cpp` that reads a list of semantic versions from standard input, sorts them in ascending order, and prints them to standard output. 

You must strictly follow these requirements:
1. **Semantic Version Comparison**: The versions are in the format `MAJOR.MINOR.PATCH` (e.g., `1.10.2`). You must correctly compare them numerically, not lexicographically (e.g., `1.10.0` is greater than `1.2.0`).
2. **Custom Data Structure**: You must implement a custom Binary Search Tree (BST) from scratch to store and sort the version strings. You may not use `std::set`, `std::map`, `std::vector`, arrays, or `std::sort` to bypass building the tree. You can parse the strings however you like, but the core storage and sorting mechanism must be your custom BST.
3. **Conditional Builds**: Your C++ code must use conditional compilation. It must check for a preprocessor macro named `PLATFORM_PREFIX`. If `PLATFORM_PREFIX` is defined, the program should prepend the value of this macro (as a string) followed by a space to every line of output. If it is not defined, it should just print the version string.

Once you have written the code:
1. Compile your program using `g++` into an executable located at `/home/user/sorter_bin`. You must pass a compiler flag to define `PLATFORM_PREFIX` as `"ORG_SYS"`.
2. Run your executable, redirecting the contents of `/home/user/versions.txt` into its standard input.
3. Redirect the standard output of your program to `/home/user/sorted_versions.log`.

Do not add any additional text, debug information, or empty lines to the output file. The output file should contain exactly the sorted list of prefixed versions, one per line.