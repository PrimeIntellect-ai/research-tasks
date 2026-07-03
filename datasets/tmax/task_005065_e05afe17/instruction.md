You are a FinOps analyst tasked with enforcing a new cloud cost optimization policy across our deployment infrastructure. You need to build a C++ validation tool and a minimal CI/CD pipeline to automatically filter and deploy infrastructure templates.

We have a directory of raw infrastructure deployment JSON files located at `/app/corpus/` (which includes both compliant and non-compliant templates). 

Additionally, the exact mandatory billing tag policy you must enforce is visually documented in `/app/policy.png`. You will need to extract the policy text from this image to know the exact key-value pair that MUST be present in the `"tags"` array of every valid deployment JSON.

Your tasks:

1. **Extract the Policy**: Read `/app/policy.png` to find the mandatory tag requirement. 
2. **C++ Classifier Tool**: Write a C++ program at `/home/user/filter.cpp` and compile it to `/home/user/filter`. 
   - The program must take a single file path as its first command-line argument.
   - It should parse the JSON file.
   - It must exit with status `0` (success) if the deployment JSON strictly contains the mandatory tag found in the policy image.
   - It must exit with status `1` (failure) if the tag is missing, mismatched, or the JSON is invalid.
3. **CI/CD Pipeline & Links**: Write a bash script `/home/user/pipeline.sh` that:
   - Compiles the C++ program.
   - Creates a directory `/home/user/approved_deployments/`.
   - Iterates over all JSON files in `/app/corpus/raw/` (you can assume this directory exists for your pipeline).
   - Uses your C++ `/home/user/filter` to test each file.
   - If a file passes, create a symbolic link to it inside `/home/user/approved_deployments/` using the original filename.
4. **Expect Automation**: Write an expect script `/home/user/auto_deploy.exp` that automates a fake interactive deployment tool (assume the tool is at `/app/fake_deployer`). The `fake_deployer` expects a directory path as an argument, and prompts `Are you sure you want to deploy X files? (y/n): `. Your expect script must run the tool with `/home/user/approved_deployments/` and automatically send `y`.

To verify your solution, our test suite will directly run your `/home/user/filter` binary against two hidden corpora of JSON files to ensure it perfectly identifies compliant and non-compliant deployments.