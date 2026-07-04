We are experiencing a severe reliability issue with our custom metric serialization agent used for monitoring uptime. Recently, the agent started hanging endlessly on certain inputs, causing monitoring gaps. 

You are provided with a local Git repository at `/home/user/metric_agent` containing the C source code for this serializer. We know that a recent commit introduced a regression causing an infinite loop during the encoding phase. 

Additionally, the vendor has provided a patched, stripped binary at `/app/reference_encoder` that correctly handles all inputs without hanging. However, they did not provide the updated source code.

Your task is to:
1. Use Git bisection in `/home/user/metric_agent` to identify the commit that introduced the infinite loop. The issue manifests when encoding specific payload lengths.
2. Analyze the bug in the serialization or loop logic.
3. Fix the C code in the repository so that the infinite loop is resolved and the serialization output perfectly matches the expected custom encoding.
4. Compile your fixed version to exactly `/home/user/monitor_fixed`.

The compiled binary `/home/user/monitor_fixed` must read from standard input and write the serialized binary data to standard output, exactly matching the behavior of `/app/reference_encoder`. The automated test will extensively fuzz your binary against the reference binary to ensure bit-exact equivalence for a wide range of input lengths and characters.

Please leave your compiled, working binary at `/home/user/monitor_fixed`.