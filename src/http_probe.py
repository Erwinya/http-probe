#!/usr/bin/env python3
"""HTTP health probe CLI — latency, status, optional JSON report."""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class ProbeResult:
    url: str
    ok: bool
    status: int | None
    elapsed_ms: float
    error: str | None = None
    bytes: int | None = None


def probe(url: str, timeout: float, method: str = "GET") -> ProbeResult:
    req = urllib.request.Request(url, method=method.upper())
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            elapsed = (time.perf_counter() - started) * 1000.0
            return ProbeResult(
                url=url,
                ok=200 <= resp.status < 400,
                status=resp.status,
                elapsed_ms=round(elapsed, 2),
                bytes=len(body),
            )
    except urllib.error.HTTPError as ex:
        elapsed = (time.perf_counter() - started) * 1000.0
        return ProbeResult(
            url=url,
            ok=False,
            status=ex.code,
            elapsed_ms=round(elapsed, 2),
            error=str(ex.reason),
        )
    except Exception as ex:  # noqa: BLE001 - CLI boundary
        elapsed = (time.perf_counter() - started) * 1000.0
        return ProbeResult(
            url=url,
            ok=False,
            status=None,
            elapsed_ms=round(elapsed, 2),
            error=str(ex),
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Probe HTTP endpoints for status and latency")
    parser.add_argument("urls", nargs="+", help="One or more URLs")
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--method", default="GET")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    args = parser.parse_args(argv)
    args.method = args.method.upper()

    if args.timeout <= 0:
        raise SystemExit("--timeout must be > 0")

    results = [probe(url, args.timeout, args.method) for url in args.urls]
    payload: list[dict[str, Any]] = [asdict(r) for r in results]

    if args.json:
        print(json.dumps({"results": payload}, indent=2))
    else:
        for r in results:
            status = r.status if r.status is not None else "-"
            flag = "OK" if r.ok else "FAIL"
            extra = f" error={r.error}" if r.error else f" bytes={r.bytes}"
            print(f"[{flag}] {r.url} status={status} {r.elapsed_ms}ms{extra}")

    return 0 if all(r.ok for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
