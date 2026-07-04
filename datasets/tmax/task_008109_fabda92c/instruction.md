I have a multi-file Rust project located at `/home/user/storage-node` that acts as a low-level storage data processor. We recently updated our internal data schema from version 1 to version 2 to include a basic error-detecting checksum, but the developer left the project in a broken state. It currently fails to compile. 

Your task is to fix the compilation errors, implement the schema migration and checksum logic, and set up a CI/CD pipeline.

Here is what you need to do:

1. **Fix Compilation & Implement Schema Migration:**
   The project has `DataBlockV1` and `DataBlockV2` defined in `src/models.rs`. The code fails to compile because it attempts to convert `DataBlockV1` to `DataBlockV2`, but the `From` trait is not implemented.
   Implement `From<DataBlockV1> for DataBlockV2` in `src/models.rs`. 
   *Migration Rules:*
   - Copy the `id` and `payload` fields directly from V1 to V2.
   - For the new `checksum` field in V2, calculate the bitwise XOR sum of all bytes in the `payload` vector. If the payload is empty, the checksum should be `0`.

2. **Implement Checksum Validation:**
   In `src/models.rs`, implement a method on `DataBlockV2` with the signature `pub fn is_valid(&self) -> bool`. This method should return `true` if the bitwise XOR sum of `self.payload` exactly matches `self.checksum`, and `false` otherwise.

3. **CI/CD Pipeline Setup:**
   Create a GitHub Actions workflow file at `/home/user/storage-node/.github/workflows/ci.yml`.
   The workflow must:
   - Trigger on `push` to the `main` branch.
   - Use `ubuntu-latest`.
   - Contain steps that run `cargo build` and `cargo test`.

4. **Verify and Generate Output:**
   Once the code compiles and tests pass, run the project binary (`cargo run`) from the `/home/user/storage-node` directory. Redirect its standard output to a file exactly at `/home/user/success.log`.

Do not modify `src/main.rs`. All your Rust code changes should be in `src/models.rs`.