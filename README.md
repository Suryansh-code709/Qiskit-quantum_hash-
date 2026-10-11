# Quantum Hash Lab

This repository implements a beginner-friendly custom Open Innovation project for the Qiskit Fall Fest 2026 Phase 1 challenge. Its domain is **quantum hash creation → quantum attack demonstration → quantum defense comparison**.

The project uses a small, transparent quantum-fingerprint model so the complete demonstration can run locally without pretending that a toy circuit is production cryptography. SHA-256 remains the classical baseline. The web application shows how a message becomes a phase-encoded fingerprint, how a small candidate domain can be searched, and why a wider digest provides a stronger generic quantum preimage margin.

## Selected problem statement

- Track: Post-Quantum Cryptography
- Code: `P-OI`
- Problem: Open Innovation — Custom PQC Problem
- Project title: `Quantum Hash Lab: Creation, Grover Attack, and Quantum-Resistant Defense`

## Why this qualifies as a custom PQC project

The official hackathon instructions require a single selected problem statement from the provided list and a reproducible Processor A vs Processor B comparison. The provided PDFs do not contain a uniquely specified hash function instance or a closed-form scoring rubric for the custom Open Innovation track; instead, they define the general rules for Phase 1 and the architecture benchmark pattern.

This project therefore implements a conservative, evidence-based custom PQC submission that:

- creates a toy phase-encoded quantum fingerprint from a message,
- demonstrates an exact attack over a deliberately tiny domain and reports the ideal Grover query estimate,
- compares an 8-bit toy profile with SHA-256 and SHA-512 defense profiles,
- studies classical SHA-256 as a baseline and measures its avalanche behavior,
- explains the difference between hashing, encryption, and a quantum fingerprint,
- runs a synthetic Processor A/B comparison using the same benchmark logic described in the guide,
- keeps all results reproducible from a clean Python environment.

## Repository structure

- `main.py` — end-to-end implementation and result generation
- `src/hash_security.py` — SHA-256 hashing, avalanche analysis, benchmarks, and Grover complexity model
- `src/quantum_hash_demo.py` — toy quantum fingerprint, attack demonstration, and defense profiles
- `src/processor_analysis.py` — synthetic Processor A/B architecture comparison
- `processors/` — processor definitions and routing metadata
- `results/tables/` — CSV/JSON tables for measured data
- `results/figures/` — generated plots
- `docs/requirements_traceability.md` — mapping from official requirements to implementation
- `report.md` — project summary and interpretation
- `tests/` — automated validation of critical logic

## Setup

```bash
python -m venv .venv
. .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
pytest -q
```

### Windows setup

```powershell
cd "C:\Users\<your-name>\qiskit-quantum-hash"
py -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
```

### Start the website

```powershell
python .\web\app.py
```

Open <http://127.0.0.1:5000> and enter a message. The site demonstrates:

1. Toy phase-encoded quantum-fingerprint creation.
2. A complete small-domain classical search and an idealized Grover query estimate.
3. Defense scaling for 8-bit, SHA-256, and SHA-512 profiles.

The toy fingerprint and attack are educational demonstrations, not production cryptography or a real hardware quantum attack.

## What the project measures

1. Toy quantum hash/fingerprint creation
2. Small-domain attack demonstration and ideal Grover estimate
3. Defense comparison for 8-, 256-, and 512-bit profiles
4. SHA-256 determinism, avalanche behavior, and runtime scaling
5. Synthetic Processor A vs Processor B routing overhead and comparison

## Important caveat

This project is designed to be compatible with the Phase 1 challenge framework, but it does not claim that the toy fingerprint is a secure replacement for SHA-256 or that the synthetic processor numbers are official hardware results. The attack is intentionally small and educational; the defense discussion explains the security scaling rather than claiming to defeat a real quantum computer.

## Create a hash from your input

```bash
python main.py "hello world"
```

The output is:

```text
Input: hello world
SHA-256: b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9
```

You can also run it interactively:

```bash
python main.py
```

The program will ask:

```text
Enter text to hash:
```

To create the benchmark tables and figures as well as hash your input, use:

```bash
python main.py "hello world" --analysis
```

The generated analysis files are saved in `results/`.

## Team workflow

Clone the repository:

```bash
git clone https://github.com/Suryansh-code709/qiskit-quantum-hash.git
cd qiskit-quantum-hash
```

Create a branch for your work:

```bash
git switch -c your-name/feature-name
```

After making changes:

```bash
python -m pytest -q
git add .
git commit -m "Describe your change"
git push -u origin your-name/feature-name
```

Open a pull request on GitHub instead of pushing directly to `main`.
