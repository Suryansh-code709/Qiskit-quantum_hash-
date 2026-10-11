from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
import time
from pathlib import Path
from typing import Any, Iterable, Sequence, Union


InputLike = Union[str, bytes, bytearray]


def normalize_bytes(data: InputLike) -> bytes:
    if isinstance(data, (bytes, bytearray)):
        return bytes(data)
    if isinstance(data, str):
        return data.encode("utf-8")
    raise TypeError(f"Unsupported input type: {type(data).__name__}")


def sha256_digest(data: InputLike) -> str:
    """Return a hexadecimal SHA-256 digest for the provided input."""
    return hashlib.sha256(normalize_bytes(data)).hexdigest()


def verify_message_integrity(message: InputLike, expected_digest: str | None = None) -> tuple[bool, str]:
    """Verify a digest and return whether it matches the expected value."""
    actual = sha256_digest(message)
    expected = expected_digest.lower() if expected_digest else actual.lower()
    return actual.lower() == expected.lower(), actual


def known_answer_tests() -> dict[str, str]:
    """Published SHA-256 test vectors. Source: FIPS 180-4 and common hashing examples."""
    return {
        "empty_string": sha256_digest(""),
        "abc": sha256_digest("abc"),
        "hello_world": sha256_digest("hello world"),
        "qiskit_fall_fest": sha256_digest("Qiskit Fall Fest 2026"),
    }


def count_bit_differences(left: str, right: str) -> int:
    if len(left) != len(right):
        raise ValueError("Digest lengths must match for bit-difference analysis.")
    left_bits = int(left, 16)
    right_bits = int(right, 16)
    return (left_bits ^ right_bits).bit_count()


def avalanche_analysis(messages: Sequence[InputLike], trials: int = 5) -> list[dict[str, Any]]:
    """Measure how many output bits change when a controlled change is applied to the input."""
    results: list[dict[str, Any]] = []
    for idx, original in enumerate(messages):
        original_digest = sha256_digest(original)
        for trial in range(1, trials + 1):
            modified = original
            if isinstance(original, str):
                changed = original + f" :: trial {trial}"
            else:
                changed = bytes(original) + b"::trial" + str(trial).encode()
            changed_digest = sha256_digest(changed)
            changed_bits = count_bit_differences(original_digest, changed_digest)
            results.append(
                {
                    "case_index": idx,
                    "trial": trial,
                    "original_digest": original_digest,
                    "modified_digest": changed_digest,
                    "changed_bits": changed_bits,
                    "changed_percent": (changed_bits / 256) * 100.0,
                }
            )
    return results


def benchmark_sha256(input_sizes: Iterable[int], trials: int = 5) -> list[dict[str, Any]]:
    """Benchmark SHA-256 runtime across selected input sizes. Returns timing samples."""
    rows: list[dict[str, Any]] = []
    for size in input_sizes:
        payload = "A" * size
        times: list[float] = []
        for _ in range(trials):
            start = time.perf_counter()
            sha256_digest(payload)
            elapsed = time.perf_counter() - start
            times.append(elapsed)
        rows.append(
            {
                "input_size_bytes": size,
                "mean_seconds": statistics.mean(times),
                "median_seconds": statistics.median(times),
                "min_seconds": min(times),
                "max_seconds": max(times),
                "trials": trials,
            }
        )
    return rows


def classical_search_space_bits() -> int:
    return 256


def grover_query_estimate(n_bits: int, desired_success: float = 0.5) -> dict[str, float]:
    """Approximate the Grover lower-bound query complexity for an n-bit hash output."""
    search_space = 1 << n_bits
    classical_work = search_space / 2.0
    quantum_work = (math.pi / 4.0) * math.sqrt(search_space)
    p_success = min(max(desired_success, 0.0), 1.0)
    return {
        "n_bits": n_bits,
        "search_space": float(search_space),
        "classical_queries": float(classical_work),
        "quantum_queries": float(quantum_work),
        "speedup_ratio": float(classical_work / quantum_work) if quantum_work else 0.0,
        "success_probability_target": float(p_success),
    }


def export_rows(path: str | Path, rows: Sequence[dict[str, Any]]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def export_json(path: str | Path, payload: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def describe_hash_security() -> dict[str, Any]:
    vectors = known_answer_tests()
    summary = {
        "sha256_digest_length_bits": 256,
        "known_answer_vectors": vectors,
        "cryptographic_note": "SHA-256 is a hash function, not encryption. It is deterministic and suitable for integrity checks, not reversible plaintext recovery.",
    }
    return summary


