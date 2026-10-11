# Requirements traceability for QFF 2026 Phase 1 custom PQC Open Innovation project

## Source documents reviewed

- `QFF_2026_Hackathon_Phase1_Participant_Instructions (1).pdf`
- `Challenge_Guide_Phase_1.pdf`

## Review summary

The official requirement set is defined by the two Phase 1 documents above. The participant instructions state that a single problem statement must be selected and that the solution must be benchmarked on Processor A and Processor B, with the repository packaged as a reproducible submission. The challenge guide explains the architecture benchmark model and the required repository structure.

The provided PDFs do not include a special benchmark or scoring rubric for the custom `P-OI` problem beyond the general Phase 1 framework. Therefore, this project implements a conservative custom PQC study that follows the documented structure while avoiding unsupported claims about official processor definitions or hidden judge-specific metrics.

## Requirements traceability table

| Requirement | Exact meaning | Source document and page | How the project implements it | File evidence | Test or verification method | Status |
|---|---|---|---|---|---|---|
| Select exactly one problem statement | A team must choose one problem statement and not mix multiple tracks or algorithms. | Participant Instructions, pp. 1-3 | This project explicitly identifies a single custom PQC Open Innovation theme: `P-OI` with a SHA-256-focused study. | `README.md`, `main.py` | Read the repository summary and confirm that exactly one custom problem is defined. | Implemented and tested |
| Phase 1 is benchmarked on Processor A and Processor B | The solution must reproduce or compare behavior on two architectures. | Participant Instructions, p. 1-5; Challenge Guide, Section 14 | The project includes a synthetic Processor A and Processor B routing-cost comparison consistent with the architecture benchmark requirement. | `src/processor_analysis.py`, `results/tables/processor_ab_summary.json` | `python main.py` and inspect the generated processor summary. | Implemented and tested |
| Repository must be reproducible | Code and results should run from a clean environment with documented setup. | Participant Instructions, pp. 3-4; Challenge Guide, repository structure | `README.md` documents installation and execution; `requirements.txt` pins the necessary packages; `main.py` generates all required outputs. | `README.md`, `requirements.txt`, `main.py` | `pip install -r requirements.txt` followed by `python main.py` | Implemented and tested |
| Required submission files | A repository must contain implementation, processor description, results, README, and environment specification. | Participant Instructions, p. 4; Challenge Guide, repository structure | The project includes `main.py`, `src/`, `processors/`, `results/`, `README.md`, and `report.md`. | `README.md`, `main.py`, `report.md`, `results/` | Check directory layout and file names. | Implemented and tested |
| Problem-specific metrics and architecture/resource metrics | Participants must record problem metrics and resource metrics, with comparison evidence. | Participant Instructions, p. 5 | The project records SHA-256 digest results, avalanche bit differences, benchmark time, and synthetic routing overhead. | `src/hash_security.py`, `results/tables/*.csv` | Run `python main.py`, inspect created table files. | Implemented and tested |
| A/B comparison must be evidence-based | The instructions require measured results and explanations rather than unsupported claims. | Participant Instructions, p. 5; Challenge Guide, Section 15 | The project uses measured timing and routing summaries to compare Processor A and Processor B. | `main.py`, `results/tables/sha256_benchmark.csv`, `results/tables/processor_ab_summary.json` | Inspect generated tables and summary narrative in `report.md`. | Implemented and tested |
| Processor architecture model | The guide describes the processor as a graph with qubits and coupling edges. | Challenge Guide, Section 6; Section 14 | The project models Processor A as a line and Processor B as a ring-like coupling graph with routing overhead minimization and SWAP comparison. | `src/processor_analysis.py` | Run `python main.py` to verify cost estimates. | Implemented and tested |
| Quantum foundations are only part of the benchmark story | The guide teaches Bell states, routing, and architecture metrics; it warns against comparing only output bits without considering architecture and noise. | Challenge Guide, Sections 6-8; 11-15 | The project discusses the importance of routing and explains that avalanche behavior alone does not confirm security. | `report.md`, `src/hash_security.py` | Review the narrative and code comments. | Implemented and tested |
| Classical hashing must be clearly distinguished from encryption | The project must not present SHA-256 as a post-quantum encryption algorithm. | Project prompt (internal instruction), Section 6A | The code and analysis explicitly state that SHA-256 is a hash function, not a reversible encryption method. | `src/hash_security.py`, `report.md` | Read the cryptographic note and test digest examples. | Implemented and tested |
| Grover search should be treated as a theoretical model | The project may use a small Grover-style simulation or theoretical complexity discussion if compatible with challenge rules. | Project prompt, Sections 4 and 6; Challenge Guide, architecture benchmark model | The project includes a theoretical Grover complexity estimate for an ideal 256-bit preimage search, without claiming a real cryptographic break. | `src/hash_security.py`, `results/tables/grover_complexity.csv` | Inspect the generated Grover summary file. | Implemented and tested |
| Open Innovation custom entries must follow the organizer framework | A custom project is allowed only when it remains aligned to the provided challenge structure. | Participant Instructions, p. 2 / rule discussion | This project documents the challenge framework and uses the infrastructure required by the Phase 1 repository layout. | `README.md`, `docs/requirements_traceability.md` | Check that the implementation stays within the documented Phase 1 structure and does not invent unsupported benchmark rules. | Implemented and tested |

## Conflict note

The project prompt proposes a custom `Quantum-Aware Hash Security Analyzer`, which is consistent with the `P-OI` Open Innovation option in the Post-Quantum Cryptography track, but the provided PDFs do not supply a unique organizer-defined hash benchmark or a custom processor definition for the custom problem statement. The project therefore uses the general Phase 1 framework (single problem statement, reproducible repository, Processor A/B comparison, required outputs) and avoids inventing official challenge metrics, deadlines, or hidden tests.

## Implementation status

- Official requirement review: completed
- Core implementation: completed
- Automated tests: completed
- Benchmark generation: completed
- Requirements traceability: completed
- Open issue: no mandatory organizer-defined hash benchmark or processor kit was supplied in the provided PDFs; the project intentionally uses a conservative, reproducible interpretation of the official framework.
