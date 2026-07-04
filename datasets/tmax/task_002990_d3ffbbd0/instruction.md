You are an operations engineer triaging an incident in a forensic artifact processing pipeline. Our automated containerized pipeline is failing to build and deploy. 

The pipeline relies on a custom internal Python package with a C-extension, called `fast_forensic_hash`. The source code for this package has been vendored inside the container at `/app/vendored/fast_forensic_hash`. 

Your objectives are:
1. **Diagnose and Fix the Build Failure:** Navigate to the vendored package directory and investigate why it is failing to build. The previous logs indicated a linker error during the C-extension compilation. You must modify the package source (e.g., `setup.py` or C files) to resolve the compiler/linker errors and successfully install the package in your environment using `pip install -e .`.
2. **Implement the CLI wrapper:** Once the package is installed, write a Python script at `/home/user/analyze.py`. 
    * The script must take exactly one command-line argument: a Base64-encoded string representing a forensic artifact.
    * It must decode the Base64 string into raw bytes.
    * It must pass these bytes to the `compute_hash` function from the newly installed `fast_forensic_hash` module.
    * It must print the resulting hash as a lowercase hexadecimal string to standard output, followed by a newline.
    * It must handle invalid Base64 input gracefully by printing "INVALID_INPUT" and exiting with code 1.

We have provided a reference binary (an oracle) at `/opt/oracle/analyze_oracle` which represents the expected behavior. Your final `/home/user/analyze.py` implementation must produce bit-exact equivalent output to this oracle for any given valid or invalid input. 

Note: You do not have root access, but you have full permissions to modify the files in `/app/vendored/fast_forensic_hash` and install packages to your user environment.