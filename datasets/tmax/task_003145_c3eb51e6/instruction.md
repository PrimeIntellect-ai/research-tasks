A critical system service, `log-router.service`, is failing to start on this machine. I am an engineer trying to diagnose the issue. Looking at the logs, it seems the service's configuration parser is crashing when trying to read its routing rules.

The parsing utility relies on a custom open-source C++ library called `librouteconf` (version 2.1.0), the source of which is vendored at `/app/librouteconf-2.1.0`. I suspect someone recently modified the package or its build system incorrectly. 

Your task is to:
1. Diagnose and fix the build or source code perturbation in the vendored `librouteconf` package at `/app/librouteconf-2.1.0` so it compiles and functions correctly. You may use standard text processing tools (awk, sed, grep) or manual editing to fix the issue.
2. Recompile the library and ensure the `log-router.service` can start successfully.
3. To prove the parsing logic is fully fixed and robust, write a C++ program at `/home/user/route_canonicalizer.cpp` and compile it to `/home/user/route_canonicalizer`.
4. Your `route_canonicalizer` program must read a single routing configuration string from standard input (up to 1024 characters), parse it using the fixed `librouteconf` library, and print the canonicalized output to standard output. (The library provides a `RouteConf::parse_and_format(const std::string&)` function for this exact purpose). 
5. Ensure your compiled program links against the fixed library and returns an exit code of 0 on successful parsing, or 1 if the configuration string is completely invalid.

Ensure your script and compilation steps are idempotent and robust. The automated verification will test your `/home/user/route_canonicalizer` executable with random configuration strings to ensure it matches the expected behavior perfectly.