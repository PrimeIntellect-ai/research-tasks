You are the release manager for a massive microservices architecture. Before deployments, we must calculate the exact deployment order of thousands of interdependent services and detect any cyclic dependencies. 

Currently, we rely on a proprietary, stripped, single-threaded tool located at `/app/legacy_resolver`. It reads dependency edges from standard input and outputs either a valid deployment order or a cycle error. However, as our architecture has grown, this tool has become a severe bottleneck in our CI/CD pipeline.

Your task is to build a highly optimized, concurrent replacement in C, and rigorously test it using Go.

Here are your objectives:

1. **Reverse Engineer the Oracle:**
   Analyze `/app/legacy_resolver`. Figure out its exact input format, how it handles cycles, and the specific sorting rules it applies when multiple services can be deployed simultaneously (hint: there is a deterministic tie-breaking rule).

2. **Implement a Fast Resolver in C:**
   Write a highly optimized C program at `/home/user/resolver.c` and compile it to `/home/user/fast_resolver`. It must perfectly replicate the behavior and output format of the legacy resolver, but use efficient graph traversal algorithms (and concurrency if it helps parsing/processing) to handle massive graphs.

3. **Go-based Property Testing:**
   Write a Go testing harness at `/home/user/fuzzer.go`. Use Go concurrency patterns (goroutines and channels) to spin up parallel workers that generate random dependency graphs (both DAGs and graphs with cycles), feed them to both `/app/legacy_resolver` and `/home/user/fast_resolver`, and assert strict output equivalence. You will need to use this to ensure your C implementation is 100% correct across edge cases.

**Requirements:**
- The final binary must be located at `/home/user/fast_resolver`.
- It must accept the same standard input as the legacy binary and produce identical standard output.
- It must achieve a significant performance improvement on massive graphs. An automated benchmarking verifier will evaluate your executable against the legacy tool on a 100,000-edge graph. Your tool must be at least **4.0x faster** than the legacy tool.