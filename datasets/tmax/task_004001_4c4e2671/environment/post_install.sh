apt-get update && apt-get install -y python3 python3-pip rustc cargo binutils
    pip3 install pytest

    mkdir -p /tmp/setup
    cat << 'EOF' > /tmp/setup/backend_cgi.rs
#[no_mangle]
pub extern "C" fn secret_backdoor_handler() {
    let _token = "BDR_w3b_s3cr3t_9921_xyz";
    println!("Backdoor accessed!");
}

fn main() {
    println!("Normal web backend running.");
    // Prevent optimization of the backdoor
    let ptr = secret_backdoor_handler as *const ();
    if ptr.is_null() {
        secret_backdoor_handler();
    }
}
EOF

    useradd -m -s /bin/bash user || true
    rustc /tmp/setup/backend_cgi.rs -o /home/user/backend_cgi
    chmod +x /home/user/backend_cgi

    chmod -R 777 /home/user