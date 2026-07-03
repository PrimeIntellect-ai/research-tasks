apt-get update && apt-get install -y python3 python3-pip curl build-essential cargo rustc
    pip3 install pytest hypothesis

    mkdir -p /home/user/router_mig/validator/src
    mkdir -p /app

    cat << 'EOF' > /home/user/router_mig/validator/Cargo.toml
[package]
name = "validator"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]
EOF

    cat << 'EOF' > /home/user/router_mig/validator/src/lib.rs
use std::ffi::CStr;
use std::os::raw::c_char;

#[no_mangle]
pub extern "C" fn validate_url_checksum(data: *const c_char, chk: *const c_char) -> bool {
    if data.is_null() || chk.is_null() {
        return false;
    }
    let data_str = unsafe { CStr::from_ptr(data).to_str().unwrap() };
    let chk_str = unsafe { CStr::from_ptr(chk).to_str().unwrap() };

    // Intentional borrow checker error
    let mut s = String::from(data_str);
    let r1 = &s;
    s.push_str(" modifying");
    println!("{}", r1);

    true
}
EOF

    cat << 'EOF' > /home/user/router_mig/legacy_router.py
import urlparse
import ctypes

def parse_and_validate(url):
    lib = ctypes.CDLL('./validator/target/release/libvalidator.so')
    lib.validate_url_checksum.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    lib.validate_url_checksum.restype = ctypes.c_bool

    parsed = urlparse.urlparse(url)
    qs = urlparse.parse_qs(parsed.query)
    data = qs.get('data', [''])[0]
    chk = qs.get('chk', [''])[0]

    valid = lib.validate_url_checksum(data, chk)
    return {"valid": valid, "route": parsed.path, "params": {"data": data, "chk": chk}}
EOF

    cat << 'EOF' > /app/ref_router
#!/usr/bin/env python3
import sys
import json
import urllib.parse

def main():
    if len(sys.argv) < 2:
        sys.exit(1)
    url = sys.argv[1]
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query)
    data = qs.get('data', [''])[0]
    chk = qs.get('chk', [''])[0]

    valid = True
    print(json.dumps({"valid": valid, "route": parsed.path, "params": {"data": data, "chk": chk}}))

if __name__ == "__main__":
    main()
EOF
    chmod +x /app/ref_router

    cat << 'EOF' > /app/eval_benchmark.py
import sys
import time
import json
import subprocess
import random
import string

sys.path.append('/home/user/router_mig')
try:
    import router
except ImportError:
    print("0.0\n9999.0") # Accuracy, Time
    sys.exit(1)

def generate_url():
    data = ''.join(random.choices(string.ascii_letters, k=10))
    # Mock generation, the eval script would compute the actual valid check or random strings
    return f"http://example.com/api/v1/test?data={data}&chk=00"

urls = [generate_url() for _ in range(10000)]

# Verify correctness first (subset)
for u in urls[:100]:
    ref_out = json.loads(subprocess.check_output(['/app/ref_router', u]).decode())
    try:
        agent_out = router.parse_and_validate(u)
    except Exception:
        print("0.0\n9999.0")
        sys.exit(1)
    if ref_out != agent_out:
        print("0.0\n9999.0") # Failed accuracy
        sys.exit(1)

# Benchmark
start = time.time()
for u in urls:
    router.parse_and_validate(u)
end = time.time()

duration = end - start
# Output accuracy followed by metric (duration)
print(f"1.0\n{duration}")
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app