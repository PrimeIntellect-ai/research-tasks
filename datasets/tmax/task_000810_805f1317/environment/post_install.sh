apt-get update && apt-get install -y \
        python3 python3-pip \
        build-essential \
        cargo rustc \
        protobuf-compiler libprotobuf-dev \
        wget curl patch

    pip3 install pytest

    # Install grpcurl
    wget https://github.com/fullstorydev/grpcurl/releases/download/v1.8.8/grpcurl_1.8.8_linux_x86_64.tar.gz
    tar -xvf grpcurl_1.8.8_linux_x86_64.tar.gz -C /usr/local/bin/ grpcurl
    rm grpcurl_1.8.8_linux_x86_64.tar.gz

    # Setup C shared library
    cat << 'EOF' > /tmp/audioprocessor.c
#include <stdlib.h>
#include <string.h>

const char* process_audio_file(const char* filepath) {
    return strdup("The qwick brown fox jumps over the lazy dog, but the dog is not amused.");
}

void free_audio_string(char* ptr) {
    free(ptr);
}
EOF
    gcc -shared -fPIC -o /usr/local/lib/libaudioprocessor.so /tmp/audioprocessor.c
    mkdir -p /usr/local/include
    cat << 'EOF' > /usr/local/include/audioprocessor.h
const char* process_audio_file(const char* filepath);
void free_audio_string(char* ptr);
EOF
    ldconfig
    rm /tmp/audioprocessor.c

    # Create app directory and files
    mkdir -p /app
    touch /app/sample.wav
    cat << 'EOF' > /app/corrections.patch
--- a/raw.txt
+++ b/raw.txt
@@ -1 +1 @@
-The qwick brown fox jumps over the lazy dog, but the dog is not amused.
+The quick brown fox jumps over the lazy dog, but the dog was not amused.
EOF

    # Create user and Rust project
    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/transcription_service/src
    mkdir -p /home/user/transcription_service/proto

    cat << 'EOF' > /home/user/transcription_service/Cargo.toml
[package]
name = "transcription_service"
version = "0.1.0"
edition = "2021"

[dependencies]
tonic = "0.9"
prost = "0.11"
tokio = { version = "1.0", features = ["macros", "rt-multi-thread"] }

[build-dependencies]
tonic-build = "0.9"
EOF

    cat << 'EOF' > /home/user/transcription_service/proto/transcriber.proto
syntax = "proto3";
package transcriber;

service Transcriber {
    rpc Transcribe (TranscribeRequest) returns (TranscribeResponse);
}

message TranscribeRequest {
    string filepath = 1;
}

message TranscribeResponse {
    string transcript = 1;
}
EOF

    cat << 'EOF' > /home/user/transcription_service/build.rs
fn main() -> Result<(), Box<dyn std::error::Error>> {
    tonic_build::compile_protos("proto/transcriber.proto")?;
    // Missing linking directive: println!("cargo:rustc-link-lib=audioprocessor");
    Ok(())
}
EOF

    cat << 'EOF' > /home/user/transcription_service/src/ffi.rs
use std::ffi::{CStr, CString};
use std::os::raw::c_char;

extern "C" {
    fn process_audio_file(filepath: *const c_char) -> *const c_char;
    fn free_audio_string(ptr: *mut c_char);
}

pub fn transcribe_audio(filepath: &str) -> String {
    let c_filepath = CString::new(filepath).unwrap();
    unsafe {
        let result_ptr = process_audio_file(c_filepath.as_ptr());
        let c_str = CStr::from_ptr(result_ptr);
        // Memory leak: not calling free_audio_string(result_ptr as *mut c_char);
        c_str.to_string_lossy().into_owned()
    }
}
EOF

    cat << 'EOF' > /home/user/transcription_service/src/main.rs
use tonic::{transport::Server, Request, Response, Status};
use transcriber::transcriber_server::{Transcriber, TranscriberServer};
use transcriber::{TranscribeRequest, TranscribeResponse};
use std::sync::Mutex;

pub mod transcriber {
    tonic::include_proto!("transcriber");
}

mod ffi;

#[derive(Default)]
pub struct MyTranscriber {
    // Broken: Mutex without Arc or improper async state management
    state: Mutex<i32>,
}

#[tonic::async_trait]
impl Transcriber for MyTranscriber {
    async fn transcribe(
        &self,
        request: Request<TranscribeRequest>,
    ) -> Result<Response<TranscribeResponse>, Status> {
        let filepath = request.into_inner().filepath;

        let mut state = self.state.lock().unwrap();
        *state += 1;

        let transcript = ffi::transcribe_audio(&filepath);

        Ok(Response::new(TranscribeResponse { transcript }))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "[::1]:50051".parse()?;
    let transcriber = MyTranscriber::default();

    println!("Server listening on {}", addr);

    Server::builder()
        .add_service(TranscriberServer::new(transcriber))
        .serve(addr)
        .await?;

    Ok(())
}
EOF

    chmod -R 777 /home/user
    chmod -R 777 /app