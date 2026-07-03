You are migrating a legacy data processing pipeline from Python 2 to Python 3. As part of the migration testing, you need to verify that historical serialized data can still be read and validated correctly using the new Python 3 environment, specifically handling string-to-bytes differences.

You have been provided with a legacy Python 2 serialized file at `/home/user/migration/payload.pkl`. This file contains a pickled list of integers.

Your task is to write a Python 3 test script that reads this file and performs the following verifications:
1. **Deserialization**: Load the integer list from `/home/user/migration/payload.pkl`.
2. **Constraint Satisfaction**: Verify that the list of integers meets two strict constraints:
   - The sum of all integers in the list is exactly 277.
   - Every integer in the list is a valid prime number.
3. **Legacy Checksum Validation**: The legacy Python 2 system computed a custom checksum on the data. You must recompute this checksum in Python 3 to ensure data integrity. The legacy algorithm works as follows:
   - Convert the list of integers into a single comma-separated string (e.g., `[2, 3] -> "2,3"`).
   - Iterate over the ASCII byte values of this string.
   - The checksum is the sum of `(byte_value * (index + 1))` modulo 1024, where `index` is the 0-based index of the character in the string. Note: In Python 3, you must ensure you are operating on raw bytes, not unicode string characters, to match the Python 2 behavior.

After performing these steps, your script must create a JSON log file at `/home/user/migration/verification.json` containing the exact following structure:
```json
{
    "is_valid_constraint": true, 
    "legacy_checksum": 1234
}
```
(Replace `true` with `false` if the constraints are not met, and `1234` with your computed integer checksum). 

Execute your script to produce the output file.