# http-probe

Lightweight HTTP health probe in pure Python (stdlib only).

Checks status and latency for one or more URLs and can emit a JSON report.

## Status

Probe CLI (`src/http_probe.py`) for status and latency is in place. Packaging and tests will land in follow-up commits.

## Run

```powershell
python src\http_probe.py https://example.com --json
```

Multiple URLs:

```powershell
python src\http_probe.py https://example.com https://httpbingo.org/get --timeout 3
```

## Requirements

- Python 3.10+
- Standard library only

## License

MIT
