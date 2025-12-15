import time

from collections.abc import Callable
from statistics import mean, stdev
from typing import TypedDict

import contractions


class BenchmarkResults(TypedDict):
    avg_ms: float
    std_ms: float
    min_ms: float
    max_ms: float
    total_ms: float


def time_function(func: Callable[[], None], iterations: int = 1000) -> BenchmarkResults:
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        times.append((end - start) * 1000)

    avg = mean(times)
    std = stdev(times) if len(times) > 1 else 0
    min_time = min(times)
    max_time = max(times)

    return {
        "avg_ms": avg,
        "std_ms": std,
        "min_ms": min_time,
        "max_ms": max_time,
        "total_ms": sum(times)
    }


def benchmark_basic_expand() -> None:
    text = "you're happy and I'm sad but we'll get through it"
    contractions.expand(text)


def benchmark_large_text() -> None:
    text = """
    You're going to love this story. I'll tell you all about it.
    We'd been waiting for hours when they're finally arrived.
    It's not that we're impatient, but we'd rather be doing something else.
    They'll understand when we've explained everything to them.
    Who's going to tell them what's happened? I'd volunteer but I'm too busy.
    We'll see what happens when they've had time to think about it.
    """ * 100
    contractions.expand(text)


def benchmark_no_contractions() -> None:
    text = "This is a simple sentence with no contractions at all." * 100
    contractions.expand(text)


def benchmark_with_slang() -> None:
    text = "gonna wanna shoulda coulda ain't" * 50
    contractions.expand(text, slang=True)


def benchmark_without_slang() -> None:
    text = "gonna wanna shoulda coulda ain't" * 50
    contractions.expand(text, slang=False)


def benchmark_preview_small() -> None:
    text = "This's a test. I'd like it."
    contractions.preview(text, 10)


def benchmark_preview_large() -> None:
    text = "You're happy. I'm sad. We'll see. It's fine. They're here." * 100
    contractions.preview(text, 20)


def benchmark_add_single() -> None:
    contractions.add("testkey123", "test value")


def benchmark_add_dict() -> None:
    contractions.add_dict({"key1": "val1", "key2": "val2", "key3": "val3"})


def print_results(name: str, results: BenchmarkResults, iterations: int) -> None:
    print(f"\n{name}")
    print(f"  Iterations: {iterations}")
    print(f"  Average:    {results['avg_ms']:.4f} ms")
    print(f"  Std Dev:    {results['std_ms']:.4f} ms")
    print(f"  Min:        {results['min_ms']:.4f} ms")
    print(f"  Max:        {results['max_ms']:.4f} ms")
    print(f"  Total:      {results['total_ms']:.2f} ms")
    print(f"  Throughput: {iterations / (results['total_ms'] / 1000):.0f} ops/sec")


def main() -> None:
    print("=" * 70)
    print("Contractions Library Performance Benchmark")
    print("=" * 70)

    benchmarks = [
        ("Basic Expand (short text)", benchmark_basic_expand, 1000),
        ("Large Text Processing", benchmark_large_text, 100),
        ("No Contractions (negative case)", benchmark_no_contractions, 1000),
        ("With Slang Enabled", benchmark_with_slang, 1000),
        ("Without Slang", benchmark_without_slang, 1000),
        ("Preview Small Text", benchmark_preview_small, 1000),
        ("Preview Large Text", benchmark_preview_large, 100),
        ("Add Single Entry", benchmark_add_single, 100),
        ("Add Dictionary", benchmark_add_dict, 100),
    ]

    results_summary = []

    for name, func, iterations in benchmarks:
        print(f"\nRunning: {name}...")
        results = time_function(func, iterations)
        print_results(name, results, iterations)
        results_summary.append((name, results["avg_ms"], iterations / (results["total_ms"] / 1000)))

    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"{'Benchmark':<40} {'Avg Time':<15} {'Throughput'}")
    print("-" * 70)

    for name, avg_time, throughput in results_summary:
        print(f"{name:<40} {avg_time:>10.4f} ms  {throughput:>10.0f} ops/sec")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()

