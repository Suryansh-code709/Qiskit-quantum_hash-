# Report: Quantum Hash Lab

## Problem statement selected

- **Track:** Post-Quantum Cryptography
- **Code:** `P-OI`
- **Name:** Open Innovation — Custom PQC Problem

## Domain

The project now follows the intended workflow:

```text
Quantum hash creation → quantum attack demonstration → quantum defense comparison
```

The quantum hash is an intentionally small phase-encoded fingerprint derived from
SHA-256 bits. The small output makes a complete local demonstration possible.
It is an educational model, not a production cryptographic primitive.

## Research questions addressed

1. How can a message be represented as a toy quantum fingerprint?
2. How does a small candidate domain behave under classical search and an idealized Grover estimate?
3. How does increasing digest width change the generic quantum preimage-security margin?
4. How does SHA-256 respond to controlled input changes?
5. How do synthetic Processor A and Processor B compare under a routing-overhead model?

## Core findings

- The toy quantum fingerprint is normalized, so its amplitudes form a valid teaching state vector.
- The small-domain attack can be reproduced locally; its Grover number is an idealized query estimate, not a hardware run.
- A wider digest provides a larger generic quantum preimage margin: approximately 4 bits for the 8-bit toy, 128 bits for SHA-256, and 256 bits for SHA-512.
- SHA-256 is deterministic, and controlled input changes produce large diffusion across its 256-bit digest.
- The synthetic Processor A/B comparison shows that routing overhead depends on processor connectivity, reinforcing the Phase 1 architecture benchmark concept.

## Important validation notes

- The toy quantum fingerprint and SHA-256 are hash/fingerprint constructions, not encryption schemes.
- Avalanche behavior alone does not imply collision resistance.
- The project uses a conservative, evidence-based interpretation of the custom Open Innovation route and does not claim to have hidden organizer benchmark definitions beyond the public Phase 1 documents.
- The toy quantum hash is not claimed to be secure against real quantum computers; it exists to make creation, attack, and defense concepts visible.
