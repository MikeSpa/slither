# Slither

repo to learn/test the static analysis tools slither.


## [Usage](https://github.com/crytic/slither/wiki/Usage)

```bash
slither .
```
Slither runs all its [detectors](https://github.com/crytic/slither/wiki/Detector-Documentation) by default.

By default, no [printers](https://github.com/crytic/slither/wiki/Printer-Documentation) are run.


### Configuration

Some options can be set through a json configuration file. By default, slither.config.json is used if present (it can be changed through --config-file file.config.json).

Options passed via the CLI have priority over options set in the configuration file.

The following flags are supported:
```json
{
    "detectors_to_run": "detector1,detector2",
    "printers_to_run": "printer1,printer2",
    "detectors_to_exclude": "detector1,detector2",
    "exclude_informational": false,
    "exclude_low": false,
    "exclude_medium": false,
    "exclude_high": false,
    "json": "",
    "disable_color": false,
    "filter_paths": "file1.sol,file2.sol",
    "legacy_ast": false
}
```