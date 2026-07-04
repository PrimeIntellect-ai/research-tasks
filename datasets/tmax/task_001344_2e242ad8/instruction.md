You are an ML Engineer tasked with preparing training data and building a reproducible pipeline. We currently use a proprietary, stripped C binary located at `/app/feature_projector` to perform dimensionality reduction on 20-dimensional numerical feature vectors. The binary reads a comma-separated list of 20 floats from standard input and outputs a reduced feature vector.

Recently, our pipeline has been failing silently. We discovered that certain corrupted or adversarial data points cause `/app/feature_projector` to fail—either by returning a vector of all `NaN`s, or by crashing completely. Because the legacy binary has terrible inference performance, we cannot afford to simply run it on all incoming data to catch the bad records. 

Your task is to write a highly performant Go program that accurately predicts whether a data point is safe or malicious *without* invoking the binary.

**Instructions:**
1. **Analyze the Oracle:** Reverse-engineer, profile, or fuzz the stripped binary at `/app/feature_projector` to deduce the exact mathematical constraints that define a "clean" versus an "evil" (crashing/NaN) 20-dimensional feature vector. 
2. **Implement the Filter:** Write a Go program at `/home/user/filter.go` that implements your discovered logic.
3. **CLI Specification:** Your Go program must take a single file path as a command-line argument. The target file will contain exactly one line: a 20-dimensional feature vector (comma-separated floats).
4. **Output Format:** Your program must print exactly `CLEAN` to standard output if the vector is safe for the projector, and exactly `EVIL` if it violates the mathematical constraints you discovered.
5. **Compilation:** Compile your final solution to `/home/user/filter`.

*Note: Your Go program will be tested against a large, hidden evaluation corpus. It must process files in milliseconds and must not call the `/app/feature_projector` binary during evaluation.*