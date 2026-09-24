# Code quality and environment audit

- Overall status: **FAIL**
- Python: `3.13.5`
- Platform: `Linux-6.18.44-x86_64-with-glibc2.41`

## Artifact gates

### project-artifact
- Python files: 24
- Python LOC: 2225
- Test methods: 33
- PASS: `all_python_parses`
- PASS: `no_eval_exec_or_unsafe_deserialization`
- PASS: `no_subprocess_shell_true`
- PASS: `no_runtime_network_imports`
- PASS: `no_environment_absolute_paths`
- PASS: `no_todo_or_unimplemented_placeholders`
- PASS: `at_least_20_test_methods`
- PASS: `all_reproduction_entrypoints_present`
- PASS: `all_json_valid`
- PASS: `all_json_finite`
- PASS: `independent_oracle_modules_present`

### standalone-artifact
- Python files: 20
- Python LOC: 2070
- Test methods: 33
- PASS: `all_python_parses`
- PASS: `no_eval_exec_or_unsafe_deserialization`
- PASS: `no_subprocess_shell_true`
- PASS: `no_runtime_network_imports`
- PASS: `no_environment_absolute_paths`
- PASS: `no_todo_or_unimplemented_placeholders`
- PASS: `at_least_20_test_methods`
- FAIL: `all_reproduction_entrypoints_present`
- PASS: `all_json_valid`
- PASS: `all_json_finite`
- FAIL: `independent_oracle_modules_present`

## Cross-package comparison

- Common scientific source files: 39
- Mismatches: 0
