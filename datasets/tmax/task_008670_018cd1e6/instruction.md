You are an engineer tasked with porting a hybrid Python/Rust mathematical tool, `math_encoder`, to run in a minimal Linux environment. This tool calculates prime factors of large numbers using a Rust extension for speed, and then encodes the results using base32 in Python.

Currently, the project is broken in its new environment. Your goals are to fix the codebase, build the extension, and generate a final encoded result.

The project is located at `/home/user/math_project`. (You must create these files or assume they are provided. For the sake of this environment, please initialize the files as described below).

1. First, set up the project by creating the following files in `/home/user/math_project/`:

`Cargo.toml`:
```toml
[package]
name = "rs_math"
version = "0.1.0"
edition = "2021"

[lib]
name = "rs_math"
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "0.18.3", features = ["extension-module"] }
```

`src/lib.rs`:
```rust
use pyo3::prelude::*;

#[pyfunction]
fn get_factors(n: u64) -> PyResult<Vec<u64>> {
    let mut factors = Vec::new();
    let mut num = n;
    let mut divisor = 2;
    while num > 1 {
        if num % divisor == 0 {
            factors.push(divisor);
            num /= divisor;
        } else {
            divisor += 1;
        }
    }
    
    let debug_msg = String::from("Calculation complete");
    let _moved_msg = debug_msg;
    // BORROW CHECKER BUG: Trying to use a moved value
    println!("Status: {}", debug_msg);

    Ok(factors)
}

#[pymodule]
fn rs_math(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_factors, m)?)?;
    Ok(())
}
```

`setup.py`:
```python
from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    name="math_encoder",
    version="0.1.0",
    packages=["math_encoder"],
    rust_extensions=[RustExtension("rs_math", binding=Binding.PyO3)],
    zip_safe=False,
)
```

`math_encoder/__init__.py`:
```python
# IMPORT ORDERING BUG: This currently causes an ImportError when tests run 
# because it attempts to import the encoder before the config is loaded.
from .encoder import encode_factors
from .config import init_config

init_config()
```

`math_encoder/config.py`:
```python
def init_config():
    global IS_INITIALIZED
    IS_INITIALIZED = True
```

`math_encoder/encoder.py`:
```python
import base64
import rs_math
import math_encoder.config

# Fails if config is not initialized first
if not getattr(math_encoder.config, 'IS_INITIALIZED', False):
    raise RuntimeError("Config not initialized before encoder import!")

def encode_factors(n: int) -> str:
    factors = rs_math.get_factors(n)
    factor_str = ",".join(map(str, factors))
    return base64.b32encode(factor_str.encode('utf-8')).decode('utf-8')
```

2. **Fix the Rust Bug:** The Rust extension currently fails to compile due to a deliberate borrow checker error in `src/lib.rs`. Fix it.
3. **Fix the Python Bug:** The Python package suffers from an import ordering issue in `math_encoder/__init__.py` that breaks initialization. Fix the import order so that `init_config()` is executed before `encoder` is imported.
4. **Build and Install:** Install `setuptools-rust` via pip, then build and install the `math_encoder` package into the current Python environment.
5. **Run the Tool:** Write a short Python script at `/home/user/run_math.py` that imports `math_encoder`, calculates the encoded factors for the number `314159265`, and writes the resulting base32 string to `/home/user/final_output.txt`.

Ensure `/home/user/final_output.txt` contains exactly the base32 string and nothing else.