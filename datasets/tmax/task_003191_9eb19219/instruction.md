You are acting as a technical compliance officer auditing an access control system. You suspect a recent data migration error (resembling an implicit cross join) incorrectly linked several roles, granting unauthorized transitive access to a highly restricted resource.

The access control data is scattered across different formats in your home directory:
1. `/home/user/users.csv`: Relational list of users (`user_id,name`).
2. `/home/user/user_roles.csv`: Relational mapping of users to their direct roles (`user_id,role_id`).
3. `/home/user/roles.json`: A JSON document mapping a `role_id` to an array of other `role_id`s that it inherits permissions from.
4. `/home/user/role_resources.csv`: Relational mapping of roles to the resources they can access (`role_id,resource_id`).

Your task is to write a standalone Rust program at `/home/user/audit.rs` that reads these files, unifies the data into an in-memory graph representation, and computes the shortest access path from the user `U73` to the resource `RES-999`. 

The path should represent the chain of assignments and inheritances. For example, if U73 has role R1, which inherits R2, which has access to RES-999, the path is `U73,R1,R2,RES-999`.

Requirements:
- Do not use external crates (no `Cargo.toml`, standard library only, so parse the basic JSON string manually or using basic string manipulation since it's highly structured).
- Output the shortest path as a comma-separated list of IDs to `/home/user/violation_path.txt`.
- If there are multiple paths of the same shortest length, any of them is acceptable (though the data is designed to have one unique shortest path).
- Compile your script using `rustc /home/user/audit.rs` and execute it to produce the output file.