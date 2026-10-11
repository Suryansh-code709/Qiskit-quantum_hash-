from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from typing import Sequence


def _digest_bits(message: str, width: int = 8) -> tuple[int, ...]:
    if width < 2 or width > 256:
        raise ValueError("The demo hash width must be between 2 and 256 bits.")
    digest = hashlib.sha256(message.encode("utf-8")).digest()
    bits = tuple((byte >> (7 - bit)) & 1 for byte in digest for bit in range(8))
    return bits[:width]


def classical_toy_hash(message: str, width: int = 8) -> int:
    """Return a small digest so a complete attack can be demonstrated locally."""
    return int("".join(map(str, _digest_bits(message, width))), 2)


def quantum_fingerprint(message: str, width: int = 8) -> dict[str, object]:
    """Build a toy phase-encoded quantum fingerprint state.

    The amplitudes are a compact teaching model, not a production cryptographic
    primitive. Each digest bit controls the sign of one basis amplitude.
    """
    bits = _digest_bits(message, width)
    amplitude = 1 / math.sqrt(width)
    state = [amplitude if bit == 0 else -amplitude for bit in bits]
    return {
        "width": width,
        "bits": list(bits),
        "amplitudes": state,
        "normalization": sum(value * value for value in state),
        "label": f"|QH({width})> phase fingerprint",
    }


def grover_attack_demo(
    target_message: str,
    candidates: Sequence[str],
    width: int = 8,
) -> dict[str, object]:
    """Compare exhaustive search with a toy Grover query estimate.

    This reports the exact classical search over the supplied toy domain and
    the idealized Grover query count. It does not claim to run hardware.
    """
    target = classical_toy_hash(target_message, width)
    checked = 0
    found = None
    for candidate in candidates:
        checked += 1
        if classical_toy_hash(candidate, width) == target:
            found = candidate
            break
    domain_size = max(1, len(candidates))
    quantum_queries = max(1, math.ceil((math.pi / 4) * math.sqrt(domain_size)))
    return {
        "target_hash": f"{target:0{width // 4 + width % 4 // 4}x}" if width % 4 == 0 else format(target, "x"),
        "target_hash_decimal": target,
        "domain_size": domain_size,
        "classical_queries": checked,
        "classical_found": found,
        "ideal_grover_queries": quantum_queries,
        "quantum_speedup_estimate": checked / quantum_queries if quantum_queries else 0.0,
        "is_theoretical": True,
    }


@dataclass(frozen=True)
class DefenseResult:
    name: str
    output_bits: int
    classical_security_bits: int
    quantum_security_bits: int
    explanation: str


def defense_comparison() -> list[DefenseResult]:
    return [
        DefenseResult(
            name="Toy quantum fingerprint",
            output_bits=8,
            classical_security_bits=8,
            quantum_security_bits=4,
            explanation="Small output chosen so the attack can be demonstrated on a laptop.",
        ),
        DefenseResult(
            name="SHA-256 baseline",
            output_bits=256,
            classical_security_bits=256,
            quantum_security_bits=128,
            explanation="A generic Grover attack lowers idealized preimage security to about half the output width.",
        ),
        DefenseResult(
            name="SHA-512 defense profile",
            output_bits=512,
            classical_security_bits=512,
            quantum_security_bits=256,
            explanation="A wider digest restores an approximately 256-bit generic quantum preimage margin.",
        ),
    ]
