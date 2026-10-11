from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.hash_security import (
    avalanche_analysis,
    benchmark_sha256,
    describe_hash_security,
    export_json,
    export_rows,
    grover_query_estimate,
    sha256_digest,
)
from src.processor_analysis import build_comparison

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - optional plotting dependency
    plt = None

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
TABLES = RESULTS / "tables"
FIGURES = RESULTS / "figures"


def plot_avalanche(results: list[dict], output_path: Path) -> None:
    if plt is None:
        return
    labels = [f"case {row['case_index']}, trial {row['trial']}" for row in results]
    values = [row["changed_percent"] for row in results]
    plt.figure(figsize=(10, 4.5))
    plt.bar(labels, values, color="steelblue")
    plt.title("SHA-256 avalanche behavior for controlled input changes")
    plt.xlabel("Input-change trial")
    plt.ylabel("Output bits changed (%)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_processor_summary(summary: dict, output_path: Path) -> None:
    if plt is None:
        return
    labels = ["Processor A", "Processor B"]
    totals = [summary["Processor A"]["total_swap_cost"], summary["Processor B"]["total_swap_cost"]]
    plt.figure(figsize=(6, 4))
    plt.bar(labels, totals, color=["#4c72b0", "#dd8452"])
    plt.title("Synthetic A/B routing-cost comparison")
    plt.ylabel("Estimated SWAP overhead")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def run_project(message: str = "Qiskit Fall Fest 2026") -> dict:
    digest = sha256_digest(message)
    avalanche = avalanche_analysis(["hello", "Qiskit", "secure channel"], trials=3)
    timing = benchmark_sha256([32, 64, 128, 256, 512], trials=5)
    processor_summary = build_comparison()
    grover = grover_query_estimate(256)
    security = describe_hash_security()

    export_rows(TABLES / "sha256_avalanche.csv", avalanche)
    export_rows(TABLES / "sha256_benchmark.csv", timing)
    export_rows(TABLES / "grover_complexity.csv", [grover])
    export_json(TABLES / "processor_ab_summary.json", processor_summary)
    export_json(TABLES / "hash_security_summary.json", security)

    plot_avalanche(avalanche, FIGURES / "sha256_avalanche.png")
    plot_processor_summary(processor_summary, FIGURES / "processor_ab_routing.png")

    report = {
        "selected_problem_statement": "P-OI Open Innovation — Custom PQC Problem",
        "input_message": message,
        "sha256_digest": digest,
        "avalanche_sample": avalanche[:3],
        "hash_security_summary": security,
        "grover_model": grover,
        "processor_summary": processor_summary,
        "benchmark_rows": timing,
    }
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a SHA-256 hash for your input and run the project analysis."
    )
    parser.add_argument(
        "message",
        nargs="?",
        help="Text to hash. If omitted, you will be prompted for it.",
    )
    parser.add_argument(
        "--analysis",
        action="store_true",
        help="Also generate the benchmark tables and figures.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    message = args.message if args.message is not None else input("Enter text to hash: ")
    print(f"\nInput: {message}")
    print(f"SHA-256: {sha256_digest(message)}")

    if args.analysis:
        summary = run_project(message)
        print("\nFull analysis:")
        print(json.dumps({
            "selected_problem_statement": summary["selected_problem_statement"],
            "grover_quantum_queries": summary["grover_model"]["quantum_queries"],
            "processor_a_swap_cost": summary["processor_summary"]["Processor A"]["total_swap_cost"],
            "processor_b_swap_cost": summary["processor_summary"]["Processor B"]["total_swap_cost"],
        }, indent=2))
