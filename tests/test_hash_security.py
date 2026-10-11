import math

from src.hash_security import count_bit_differences, grover_query_estimate, sha256_digest
from src.quantum_hash_demo import (
    classical_toy_hash,
    defense_comparison,
    grover_attack_demo,
    quantum_fingerprint,
)


def test_sha256_known_answer_vector():
    assert sha256_digest("abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_sha256_deterministic():
    left = sha256_digest("Qiskit Fall Fest 2026")
    right = sha256_digest("Qiskit Fall Fest 2026")
    assert left == right


def test_sha256_accepts_user_text():
    assert sha256_digest("hello world") == (
        "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    )


def test_avalanche_detects_changed_output():
    left = sha256_digest("same")
    right = sha256_digest("same!")
    assert count_bit_differences(left, right) > 0
    assert count_bit_differences(left, right) < 256


def test_grover_estimate_has_expected_ordering():
    estimate = grover_query_estimate(8)
    assert estimate["classical_queries"] > estimate["quantum_queries"] > 0


def test_toy_quantum_fingerprint_is_normalized():
    fingerprint = quantum_fingerprint("hello world")
    assert fingerprint["width"] == 8
    assert math.isclose(fingerprint["normalization"], 1.0)


def test_toy_attack_finds_target_in_demo_domain():
    candidates = ["wrong", "hello world"]
    result = grover_attack_demo("hello world", candidates)
    assert result["classical_found"] == "hello world"
    assert result["target_hash_decimal"] == classical_toy_hash("hello world")


def test_wider_digest_defense_has_more_quantum_security():
    profiles = defense_comparison()
    assert profiles[0].quantum_security_bits < profiles[-1].quantum_security_bits
