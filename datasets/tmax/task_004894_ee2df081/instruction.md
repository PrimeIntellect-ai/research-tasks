We are upgrading our legacy network intrusion detection system. The previous packet inspection module was written in Ruby (`/home/user/legacy/parser.rb`), but it is too slow to handle our new throughput requirements.

You need to rewrite this detector as a high-performance C++ command-line tool located at `/home/user/detector`.

Here is the situation:
1. **The SDK:** We have two proprietary C shared libraries at `/app/sdk/`: `libpacket.so` and `libcrypto.so`. The headers are in `/app/sdk/include/`. 
   There is a known architectural bug in this SDK: `libpacket.so` depends on `crypto_validate()` from `libcrypto.so`, but `libcrypto.so` simultaneously depends on `packet_get_meta()` from `libpacket.so`. You must figure out how to successfully link against both of them in your C++ build despite this circular dependency.
2. **Serialization and Translation:** You must translate the byte-level deserialization logic found in `/home/user/legacy/parser.rb` into your C++ implementation. The packets are binary files. You will need to carefully handle the struct packing and endianness as defined in the Ruby script, and pass the unpacked buffers to the C SDK functions.
3. **The Oracle:** We have provided a stripped, vendor-supplied compiled binary at `/app/oracle_stripped` which perfectly implements the classification logic but cannot be used in production due to licensing restrictions. You can use it as a black-box oracle to understand how edge cases are handled.
4. **The Corpora:** We have provided thousands of test packets. 
   - Valid, safe packets are in `/app/corpora/clean/`
   - Malicious packets are in `/app/corpora/evil/`

Your final executable must be located at `/home/user/detector`. It must take a single argument (the file path to a packet). 
- If the packet is valid/clean, it must exit with code `0`.
- If the packet is malicious/evil, it must exit with code `1`.
- If the packet is malformed (fails deserialization), it must exit with code `2`.

Write your code, compile it using the correct linker flags to handle the circular dependency, and ensure it correctly classifies the provided corpora.