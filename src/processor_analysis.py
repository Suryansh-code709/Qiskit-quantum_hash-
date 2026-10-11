from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


@dataclass(frozen=True)
class ProcessorSpec:
    name: str
    num_qubits: int
    coupling_map: list[tuple[int, int]]
    description: str


def line_processor() -> ProcessorSpec:
    qubits = 6
    coupling = [(i, i + 1) for i in range(qubits - 1)]
    return ProcessorSpec(
        name="Processor A",
        num_qubits=qubits,
        coupling_map=coupling,
        description="A linear architecture with nearest-neighbor connectivity and low routing overhead.",
    )


def ring_processor() -> ProcessorSpec:
    qubits = 6
    coupling = [(i, (i + 1) % qubits) for i in range(qubits)]
    return ProcessorSpec(
        name="Processor B",
        num_qubits=qubits,
        coupling_map=coupling,
        description="A ring-like connectivity with more spatial flexibility but additional routing demands for long-range interactions.",
    )


def shortest_path(graph: Sequence[tuple[int, int]], start: int, end: int) -> int:
    edges = {}
    for a, b in graph:
        edges.setdefault(a, set()).add(b)
        edges.setdefault(b, set()).add(a)
    queue = [(start, 0)]
    seen = {start}
    while queue:
        node, distance = queue.pop(0)
        if node == end:
            return distance
        for neighbor in sorted(edges.get(node, set())):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append((neighbor, distance + 1))
    return math.inf


def routing_summary(processor: ProcessorSpec, logical_edges: Iterable[tuple[int, int]]) -> dict[str, Any]:
    total_swap_cost = 0
    max_distance = 0
    entries: list[dict[str, Any]] = []
    for left, right in logical_edges:
        if left >= processor.num_qubits or right >= processor.num_qubits or left < 0 or right < 0:
            raise ValueError(f"Logical edge {left}-{right} is outside processor range for {processor.name}.")
        distance = shortest_path(processor.coupling_map, left, right)
        max_distance = max(max_distance, distance)
        swap_cost = max(0, (distance - 1) * 2)
        total_swap_cost += swap_cost
        entries.append(
            {
                "logical_edge": [left, right],
                "physical_distance": distance,
                "swap_overhead": swap_cost,
            }
        )
    return {
        "processor": processor.name,
        "num_qubits": processor.num_qubits,
        "coupling_edges": len(processor.coupling_map),
        "logical_edges": list(logical_edges),
        "edges_summary": entries,
        "total_swap_cost": total_swap_cost,
        "max_physical_distance": max_distance,
        "description": processor.description,
    }


def export_processor_summary(path: str | Path, summary: Sequence[dict[str, Any]]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)


def build_comparison() -> dict[str, Any]:
    processor_a = line_processor()
    processor_b = ring_processor()
    logical_edges = [(0, 2), (1, 3), (2, 4)]
    a_summary = routing_summary(processor_a, logical_edges)
    b_summary = routing_summary(processor_b, logical_edges)
    return {
        "Processor A": a_summary,
        "Processor B": b_summary,
    }
