# http-probe

Lightweight HTTP health probe in pure Python (stdlib only).

Checks status and latency for one or more URLs and can emit a JSON report.

## Status

Probe CLI and unit tests are in place. Packaging/CI will land in follow-up commits.

## Run

```powershell
python src\http_probe.py https://example.com --json
```

## Tests

```powershell
python -m unittest discover -s tests -v
```

## Requirements

- Python 3.10+
- Standard library only

## License

MIT
