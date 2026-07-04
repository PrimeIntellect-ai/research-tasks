You are tasked with migrating a legacy Python 2 C-extension to Python 3 and adding conditional build capabilities.

You have inherited a project in the directory `/home/user/math_extension`. It contains a C-extension that evaluates simple prefix mathematical expressions (e.g., `+ 3 4`). The extension is written using the obsolete Python 2 C API and is built via `setup.py`.

Your objectives are:

1. **Migrate the C Code to Python 3:**
   Modify `/home/user/math_extension/c_math.c` to use the Python 3 C API. Specifically, you need to replace `Py_InitModule` with `PyModule_Create` and `PyModuleDef`, and update any Python 2 integer/string parsing functions (like `PyInt_FromLong`) to their Python 3 equivalents (like `PyLong_FromLong`).

2. **Implement Conditional Compilation in C:**
   Modify `c_math.c` so that if the macro `LITE_MODE` is defined during compilation, the `eval_expr` function rejects division operations (the `/` operator) by immediately returning `-999`. If `LITE_MODE` is not defined, division should proceed normally (standard integer division).

3. **Update Build Orchestration:**
   Modify `/home/user/math_extension/setup.py` to support conditionally passing the `LITE_MODE` macro. The build script must check the environment variable `BUILD_MODE`. If `BUILD_MODE=lite`, it must add the `LITE_MODE` macro definition to the C extension compiler arguments.

4. **Build, Test, and Log:**
   You must compile and install the module for Python 3 twice (e.g., using `python3 setup.py install --user`), and log the evaluation of a division operation to `/home/user/run.log`.

   Step A: Build the module with `BUILD_MODE=lite`. Run a Python 3 script that evaluates `"/ 10 2"` using the compiled extension. Append the integer result to `/home/user/run.log`.
   Step B: Build the module with `BUILD_MODE=full` (or no `BUILD_MODE`). Run a Python 3 script that evaluates `"/ 10 2"` using the compiled extension. Append the integer result to `/home/user/run.log`.

The final `/home/user/run.log` must contain exactly two lines with the integer outputs from Step A and Step B respectively.

*Note: You may need to install `python3-dev` or `python3-setuptools` if they are not already installed on your system.*