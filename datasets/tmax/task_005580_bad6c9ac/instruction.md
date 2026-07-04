You are a mobile build engineer maintaining a build pipeline for a Web Security tool. The team is migrating a security token validator to run natively on a lightweight mobile environment. 

Currently, the project is located in `/home/user/build_env/`. If you run `make`, the build fails with a linker error: `undefined reference to 'resolve_deps'`. 

The original developer wrote the dependency graph resolution logic in Go (`resolver.go`) to take advantage of goroutines and channels for concurrent graph traversal. However, they realized the mobile target cannot bundle the Go runtime. 

Your task is to:
1. Analyze the graph traversal logic in `/home/user/build_env/resolver.go`.
2. Translate this logic into C, creating a new file `/home/user/build_env/resolver.c`. Implement the function `int resolve_deps(int matrix[5][5], int num_nodes, int start_node);`. You do not need to use C concurrency (like pthreads); a synchronous functional equivalent that yields the same mathematical result is perfectly acceptable.
3. Update the `/home/user/build_env/Makefile` so that `resolver.c` is compiled and linked into the final executable named `validator`.
4. Run `make` to successfully build the executable.
5. Run `./validator > /home/user/build_env/output.log`.

Ensure that the resulting `/home/user/build_env/output.log` contains the exact output produced by your translated function as printed by `main.c`.