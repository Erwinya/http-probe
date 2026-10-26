# http-probe

Lightweight HTTP health probe in pure Python (stdlib only).

Checks status and latency for one or more URLs and can emit a JSON report.

## Status

Complete: CLI, unit tests, packaging, and CI.

## Run

```powershell
python src\http_probe.py https://example.com --json
```

Install locally (optional):

```powershell
pip install -e .
http-probe https://example.com --json
```

Exit codes: `0` when every probe succeeds, `1` when any probe fails.


PowerShell: after a run, check `0` (`0` ok, `1` any failure).


PowerShell: after a run, check `0` (`0` ok, `1` any failure).

## Options

| Flag | Default | Meaning |
|------|---------|---------|
| `--timeout` | `5.0` | Request timeout in seconds |
| `--method` | `GET` | HTTP method (for example `HEAD`) |
| `--json` | off | Emit a JSON report |

## Tests

```powershell
python -m unittest discover -s tests -v
```

## Requirements

- Python 3.10+
- Standard library only

## License

MIT
