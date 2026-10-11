from __future__ import annotations

from pathlib import Path
import sys

from flask import Flask, render_template, request

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.hash_security import (
    sha256_digest,
    count_bit_differences,
    grover_query_estimate,
    avalanche_analysis,
)
from src.quantum_hash_demo import (
    defense_comparison,
    grover_attack_demo,
    quantum_fingerprint,
)

app = Flask(__name__, template_folder=str(Path(__file__).parent / "templates"), static_folder=str(Path(__file__).parent / "static"))


@app.route("/", methods=["GET"]) 
def index():
    return render_template("index.html")


@app.route("/hash", methods=["POST"])
def do_hash():
    message = request.form.get("message", "")
    message = message.strip()
    if not message:
        return render_template("index.html", error="Please enter some text to hash.")

    digest = sha256_digest(message)
    quantum_hash = quantum_fingerprint(message)
    candidates = [message[:index] + suffix for index in range(1, len(message) + 1) for suffix in ("0", "1")]
    if message not in candidates:
        candidates.append(message)
    attack = grover_attack_demo(message, candidates)

    # Simple controlled change for avalanche demonstration: append a single character
    modified = message + "0"
    modified_digest = sha256_digest(modified)
    changed_bits = count_bit_differences(digest, modified_digest)
    changed_percent = (changed_bits / 256.0) * 100.0

    # Small sample avalanche (3 trials) for display
    avalanche = avalanche_analysis([message], trials=3)

    # Grover theoretical estimate for 256-bit hash
    grover = grover_query_estimate(256)

    # Explanatory text (kept concise and honest)
    explanation = (
        "This page creates a toy phase-encoded quantum fingerprint, then compares a real "
        "classical search of a tiny demonstration domain with an idealized Grover query estimate. "
        "The toy hash is intentionally small and is not production cryptography. "
        "SHA-256 remains the classical baseline; a wider digest is shown as the defense profile."
    )

    return render_template(
        "result.html",
        message=message,
        digest=digest,
        modified=modified,
        modified_digest=modified_digest,
        changed_bits=changed_bits,
        changed_percent=changed_percent,
        avalanche=avalanche,
        grover=grover,
        quantum_hash=quantum_hash,
        attack=attack,
        defenses=defense_comparison(),
        explanation=explanation,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
