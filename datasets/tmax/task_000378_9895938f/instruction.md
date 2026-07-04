You are tasked with fixing a failing build for a mathematical expression evaluation pipeline and creating a safety filter for user-provided mathematical formulas. 

Currently, our build pipeline is failing, and our formula database has been corrupted. You must complete three phases to restore the system:

**Phase 1: Package Debugging and Floating-Point Precision Repair**
We vendor a third-party C library for math evaluation at `/app/tinyexpr`. However, a junior developer recently modified its build configuration, and now `make test` fails with a floating-point precision assertion error. 
1. Analyze the build failure in `/app/tinyexpr`. 
2. Identify the compiler flag or configuration causing the floating-point inaccuracy.
3. Fix the build configuration so that `make test` passes successfully.

**Phase 2: Database Recovery**
We had an SQLite database at `/app/data/formulas.db` containing historically safe and unsafe mathematical expressions. The main database file's header was overwritten/corrupted, but the Write-Ahead Log (`formulas.db-wal`) is fully intact.
1. Recover the data from the WAL file.
2. The database contains two tables: `clean_formulas` and `evil_formulas`, each with a single text column `expression`.
3. Extract the expressions. Create two directories: `/home/user/clean/` and `/home/user/evil/`. Write each expression from `clean_formulas` into a separate text file in `/home/user/clean/` (e.g., `1.txt`, `2.txt`), and do the same for `evil_formulas` in `/home/user/evil/`.

**Phase 3: Formula Classifier / Filter**
We need to prevent unsafe expressions from crashing our newly fixed library.
Write an executable script at `/home/user/filter_expr` (you may write this in any language you choose, Python, Bash, C++, etc.). 
- The script must take exactly one argument: the absolute path to a text file containing a mathematical expression.
- The script must evaluate or analyze the expression.
- **Pass condition:** If the expression is mathematically valid, evaluates to a finite real number, and does not cause division by zero, NaN, or Infinity, your script must exit with status code `0`.
- **Reject condition:** If the expression evaluates to NaN, Infinity, causes a division by zero, or contains malformed operations, your script must exit with status code `1`.

You can test your script against the formulas you recovered in Phase 2. An automated verification suite will subsequently test your `/home/user/filter_expr` against a hidden adversarial corpus.