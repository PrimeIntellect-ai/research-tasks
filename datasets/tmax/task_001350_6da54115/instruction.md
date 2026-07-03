You are an on-call engineer responding to a critical 3am page. Our high-performance math processing container is failing to build, and the previous version is producing core dumps in production. 

Here is the situation:
1. We have an image at `/app/equation.png` containing a specific mathematical polynomial that our system needs to evaluate. 
2. There is a broken Python C-extension build environment in `/home/user/math_service/` that is failing to compile due to missing dependencies and syntax errors in the `setup.py`.
3. Inside `/home/user/math_service/`, there is a core dump (`core.dump`) from the previous production run. The C-extension had a buffer overflow when processing certain large inputs. 

Your task is to:
1. Extract the exact mathematical formula from `/app/equation.png` (tesseract is available).
2. Diagnose and fix the build failure in `/home/user/math_service/`.
3. Analyze the core dump to understand the nature of the crash (you can use `gdb` with Python extensions or standard analysis tools).
4. Write a robust Python script at `/home/user/evaluate.py` that takes a single integer argument `x` from the command line, evaluates the polynomial extracted from the image, and prints the result to standard output. 

The script must correctly handle the polynomial calculation without crashing, effectively replacing the buggy C-extension logic for this specific equation. The script will be rigorously fuzzed with thousands of random inputs to ensure it perfectly matches the expected mathematical output.