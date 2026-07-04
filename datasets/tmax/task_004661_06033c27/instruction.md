I need help setting up a polyglot build process for a data integration pipeline. We have a mathematical checksum/Forward Error Correction (FEC) algorithm written in C, and we need to use it within a Rust application that processes Protobuf messages.

Here is the setup in the directory `/home/user/workspace`:

1.  `checksum.c`: Contains our proprietary FEC algorithm.
    ```c
    #include <stdint.h>
    #include <stddef.h>

    uint32_t compute_fec(const uint8_t* data, size_t len) {
        uint32_t fec = 0x12345678;
        for (size_t i = 0; i < len; i++) {
            fec ^= data[i];
            fec = (fec << 5) | (fec >> 27);
        }
        return fec;
    }
    ```
2.  `message.proto`: The protobuf schema for our data payloads.
    ```proto
    syntax = "proto3";
    package polyglot;

    message MessageRecord {
        bytes payload = 1;
        uint32 fec = 2;
    }
    ```
3.  A Rust project has been initialized in `/home/user/workspace/rs_app`. The `Cargo.toml` already contains the necessary dependencies (`prost`, `prost-build`, `cc`).

Your task is to:
1.  Create `/home/user/workspace/rs_app/build.rs` to orchestrate a polyglot build. It must:
    *   Compile `message.proto` into Rust code (using `prost_build`).
    *   Compile `../checksum.c` into a static library named `libchecksum.a` and link it (using the `cc` crate).
2.  Write `/home/user/workspace/rs_app/src/main.rs`. It must:
    *   Include the generated protobuf Rust code.
    *   Declare the foreign C function `compute_fec` using FFI.
    *   Create a `MessageRecord` where the `payload` is the exact byte string `"INTEGRATION_TEST_DATA"`.
    *   Calculate the `fec` field by passing the payload to the C FFI function.
    *   Serialize the `MessageRecord` using Prost and write the raw binary output to `/home/user/workspace/output.bin`.

Once the code is written, build and run the Rust application so that `/home/user/workspace/output.bin` is created. Do not output anything else; just ensure the binary file is produced at the exact path specified.